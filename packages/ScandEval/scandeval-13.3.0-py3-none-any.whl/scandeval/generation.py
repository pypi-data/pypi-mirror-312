"""Functions related to text generation of models."""

import logging
import sys
import warnings
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import torch
from datasets import Dataset
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import (
    GenerationConfig,
    PreTrainedTokenizerBase,
    StoppingCriteria,
    StoppingCriteriaList,
)
from transformers.modeling_utils import ModelOutput

from .exceptions import InvalidBenchmark
from .model_cache import (
    ModelCache,
    load_cached_model_outputs,
    split_dataset_into_cached_and_non_cached,
)
from .openai_models import OpenAIModel
from .structured_generation_utils import (
    get_ner_logits_processors,
    get_ner_prefix_allowed_tokens_fn,
)
from .tasks import LA, NER, RC, SENT, SUMM
from .utils import SUPERTASKS_USING_LOGPROBS, clear_memory, get_end_of_chat_token_ids
from .vllm_models import VLLMModel

if TYPE_CHECKING:
    from transformers import DataCollator

    from .config import BenchmarkConfig, DatasetConfig, ModelConfig
    from .protocols import GenerativeModel, Tokenizer

logger = logging.getLogger(__package__)


def generate(
    itr: tqdm,
    prepared_train: Dataset,
    prepared_tests: list[Dataset],
    model: "GenerativeModel",
    model_config: "ModelConfig",
    tokenizer: "Tokenizer",
    data_collator: "DataCollator",
    compute_metrics: Callable,
    extract_labels_fn: Callable[..., list[Any]],
    benchmark_config: "BenchmarkConfig",
    dataset_config: "DatasetConfig",
) -> dict[str, list[dict[str, float]]]:
    """Evaluate a model on a dataset through generation.

    Args:
        itr:
            The progress bar iterator.
        prepared_train:
            The prepared training dataset.
        prepared_tests:
            The prepared bootstrapped test datasets.
        num_iter:
            The number of iterations to run.
        rng:
            The random number generator.
        model:
            The model to evaluate.
        model_config:
            The configuration of the model.
        tokenizer:
            The tokenizer to use for the model. If `None` then the model's
            tokenizer will be used.
        data_collator:
            The data collator to use for the model.
        compute_metrics:
            The function to use to compute the metrics.
        extract_labels_fn:
            The function to use to extract the labels from the model output.
        benchmark_config:
            The configuration of the benchmark.
        dataset_config:
            The configuration of the dataset.

    Returns:
        A dictionary containing the scores, with keys "test" and maybe "train", with
        values being lists of dicts containing the scores for each metric for each
        iteration.
    """
    scores: dict[str, list[dict[str, float]]] = defaultdict(list)

    # Set up the name of the model output cache. If we are testing then we save the
    # model outputs to a different cache and ensure that that cache is deleted before
    # the next test, to ensure that the tests are independent of each other
    if benchmark_config.debug:
        model_cache_dir = Path.cwd()
    else:
        model_cache_dir = Path(model_config.model_cache_dir)
    if hasattr(sys, "_called_from_test"):
        cache_name = f"{dataset_config.name}-model-outputs-test.json"
        (model_cache_dir / cache_name).unlink(missing_ok=True)
    elif benchmark_config.debug:
        cache_name = f"{model_config.model_id}-{dataset_config.name}-model-outputs.json"
    else:
        cache_name = f"{dataset_config.name}-model-outputs.json"

    cache = ModelCache(
        model_cache_dir=model_cache_dir,
        cache_name=cache_name,
        max_generated_tokens=dataset_config.max_generated_tokens,
    )

    for idx in itr:
        prepared_test = prepared_tests[idx]
        assert isinstance(prepared_test, Dataset)

        generation_kwargs = dict(
            model=model,
            tokenizer=tokenizer,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
            extract_labels_fn=extract_labels_fn,
            dataset_config=dataset_config,
            cache=cache,
        )

        def update_scores(
            scores: dict[str, list[dict[str, float]]],
            benchmark_config: "BenchmarkConfig",
        ) -> dict[str, list[dict[str, float]]]:
            """Perform a single iteration of generation and update the scores.

            Args:
                scores:
                    The scores so far.
                benchmark_config:
                    The configuration of the benchmark.

            Returns:
                The updated scores.
            """
            test_scores = generate_single_iteration(
                prepared_dataset=prepared_test,
                benchmark_config=benchmark_config,
                **generation_kwargs,
            )
            logger.debug(f"Test scores for iteration {idx}: {test_scores}")
            scores["test"].append(test_scores)

            if benchmark_config.evaluate_train:
                train_scores = generate_single_iteration(
                    prepared_dataset=prepared_train,
                    benchmark_config=benchmark_config,
                    **generation_kwargs,
                )
                logger.debug(f"Train scores for iteration {idx}: {train_scores}")
                scores["train"].append(train_scores)

            clear_memory()
            return scores

        if isinstance(model, VLLMModel):
            scores = update_scores(scores=scores, benchmark_config=benchmark_config)
        else:
            while True:
                try:
                    scores = update_scores(
                        scores=scores, benchmark_config=benchmark_config
                    )
                    break
                except Exception as e:
                    oom_error = [
                        "CUDA out of memory",
                        "CUDA error",
                        "MPS backend out of memory",
                        "Too many parallel completions requested.",  # OpenAI specific
                    ]
                    if isinstance(model, VLLMModel) or all(
                        error not in str(e) for error in oom_error
                    ):
                        raise InvalidBenchmark(str(e))
                    clear_memory()
                    benchmark_config.batch_size //= 2
                    if benchmark_config.batch_size < 1:
                        raise InvalidBenchmark(
                            "GPU out of memory, even with a batch size of 1!"
                        )

    if not benchmark_config.debug:
        cache.remove()

    return scores


def generate_single_iteration(
    prepared_dataset: Dataset,
    model: "GenerativeModel",
    tokenizer: "Tokenizer",
    data_collator: "DataCollator",
    compute_metrics: Callable,
    extract_labels_fn: Callable[..., list[Any]],
    dataset_config: "DatasetConfig",
    benchmark_config: "BenchmarkConfig",
    cache: ModelCache,
) -> dict[str, float]:
    """Evaluate a model on a dataset in a single iteration through generation.

    Args:
        prepared_dataset:
            The dataset to evaluate on.
        model:
            The model to evaluate.
        tokenizer:
            The tokenizer to use for the model.
        data_collator:
            The data collator to use for the model.
        compute_metrics:
            The function to use to compute the metrics.
        extract_labels_fn:
            The function to use to extract the labels from the dataset.
        dataset_config:
            The configuration of the dataset.
        benchmark_config:
            The configuration of the benchmark.
        cache:
            The model output cache.

    Returns:
        A list of dictionaries containing the scores for each metric.
    """
    cache.load()

    # Split up the prepared dataset into a cached and non-cached part
    cached_dataset, non_cached_dataset = split_dataset_into_cached_and_non_cached(
        dataset=prepared_dataset, cache=cache
    )

    all_preds: list[dict | str | list[str]] = list()

    if len(non_cached_dataset) > 0:
        # Tokens used in generation to know when generation is finished
        stopping_criteria = get_generation_stopping_criteria(
            tokenizer=tokenizer, model=model
        )

        generation_config = GenerationConfig(
            # What to output
            max_new_tokens=dataset_config.max_generated_tokens,
            output_scores=dataset_config.task.supertask in SUPERTASKS_USING_LOGPROBS,
            return_dict_in_generate=True,
            # How to sample
            do_sample=False,  # Equivalent to greedy decoding (temperature=0)
            # Special tokens
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

        # Sort the non_cached dataset by the length of the text, to minimise the amount
        # of padding that needs to be added, speeding up generation
        non_cached_dataset = non_cached_dataset.add_column(
            name="length", column=[len(x) for x in non_cached_dataset["text"]]
        )
        non_cached_dataset = non_cached_dataset.sort("length", reverse=True)

        # Enable batching by building a dataloader. The dataloader cannot deal with
        # text columns, so we create a copy of the dataset without these
        torch_dataset = non_cached_dataset.with_format("torch").remove_columns(
            [
                column
                for column in non_cached_dataset.column_names
                if column != "input_ids"
            ]
        )

        if isinstance(model, OpenAIModel):
            batch_size = 1
        elif isinstance(model, VLLMModel):
            batch_size = len(torch_dataset)
        else:
            batch_size = benchmark_config.batch_size

        dataloader = DataLoader(
            dataset=torch_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=4,
            collate_fn=data_collator,
        )

        with warnings.catch_warnings():
            # This ignores the following warning, which is out of our control:
            #   "os.fork() was called. os.fork() is incompatible with multithreaded
            #   code, and JAX is multithreaded, so this will likely lead to a deadlock."
            warnings.simplefilter("ignore", category=RuntimeWarning)

            itr = (
                dataloader
                if batch_size == len(torch_dataset) or hasattr(sys, "_called_from_test")
                else tqdm(iterable=dataloader, leave=False)
            )

            # Generate the completions for the non-cached examples
            for batch_idx, batch in enumerate(itr):
                model_output, extracted_labels = generate_batch(
                    batch=batch,
                    batch_idx=batch_idx,
                    batch_size=batch_size,
                    non_cached_dataset=non_cached_dataset,
                    model=model,
                    tokenizer=tokenizer,
                    stopping_criteria=stopping_criteria,
                    generation_config=generation_config,
                    extract_labels_fn=extract_labels_fn,
                    dataset_config=dataset_config,
                )

                # Extended logging if we are running in debug mode
                if benchmark_config.debug:
                    debug_log(
                        batch_idx=batch_idx,
                        batch_size=batch_size,
                        non_cached_dataset=non_cached_dataset,
                        extracted_labels=extracted_labels,
                        dataset_config=dataset_config,
                    )

                cache.add_to_cache(
                    model_input=batch["input_ids"],
                    model_output=model_output,
                    tokenizer=tokenizer,
                )
                all_preds.extend(extracted_labels)

                # If we are debugging then we save the cache often, but since this makes
                # evaluation slower, we do not do this by default
                if benchmark_config.debug:
                    cache.save()

        if isinstance(itr, tqdm):
            itr.close()

        # Store the cache to disk
        cache.save()

    # Fetch the cached predictions for the cached examples
    if len(cached_dataset) > 0:
        model_output = load_cached_model_outputs(
            cached_dataset=cached_dataset, cache=cache, tokenizer=tokenizer
        )
        extracted_labels = extract_labels_fn(
            input_batch=cached_dataset, model_output=model_output, tokenizer=tokenizer
        )
        all_preds.extend(extracted_labels)

    if "label" in non_cached_dataset.column_names:
        ground_truth = [
            label.lower() if isinstance(label, str) else label
            for label in non_cached_dataset["label"] + cached_dataset["label"]
        ]
    elif "labels" in non_cached_dataset.column_names:
        ground_truth = [
            [label.lower() if isinstance(label, str) else label for label in label_list]
            for label_list in non_cached_dataset["labels"] + cached_dataset["labels"]
        ]
    elif "target_text" in non_cached_dataset.column_names:
        ground_truth = non_cached_dataset["target_text"] + cached_dataset["target_text"]
    else:
        raise ValueError(
            "The dataset must have either a 'label', 'labels', or 'target_text' column"
        )

    itr_scores: dict[str, float] = compute_metrics(
        model_outputs_and_labels=(all_preds, ground_truth),
        id2label=dataset_config.id2label,
    )

    return itr_scores


class StopWordCriteria(StoppingCriteria):
    """Stopping criteria for generation based on stop words.

    Attributes:
        stop_word_id_lists:
            A list of lists of token IDs that are used to determine whether generation
            should stop.
        indices_done:
            A list of indices of the examples for which generation has already stopped.
            Resets every batch.
    """

    def __init__(self, stop_word_id_lists: list[list[int]]):
        """Initialize the stopping criteria.

        Args:
            stop_word_id_lists:
                A list of lists of token IDs that are used to determine whether
                generation should stop.
        """
        super().__init__()
        self.stop_word_id_lists = stop_word_id_lists
        self.indices_done: list[int] = list()

    def clear(self) -> None:
        """Clear the example indices for which generation has already stopped."""
        self.indices_done = list()

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        """Determine whether generation should stop.

        Args:
            input_ids:
                The input IDs of the generated sequences.
            scores:
                The scores of the generated sequences. Not used.
            **kwargs:
                Additional keyword arguments. Not used.

        Returns:
            Whether generation should stop.
        """
        for stop_word_id_list in self.stop_word_id_lists:
            for batch_idx in range(input_ids.shape[0]):
                inputs = input_ids[batch_idx].tolist()
                sample_ends_with_stop_word = (
                    inputs[-len(stop_word_id_list) :] == stop_word_id_list
                )
                if sample_ends_with_stop_word:
                    self.indices_done.append(batch_idx)
                if all(idx in self.indices_done for idx in range(input_ids.shape[0])):
                    return True
        return False


def generate_batch(
    batch: dict[str, torch.Tensor],
    batch_idx: int,
    batch_size: int,
    non_cached_dataset: Dataset,
    model: "GenerativeModel",
    tokenizer: "Tokenizer",
    stopping_criteria: StopWordCriteria,
    generation_config: GenerationConfig,
    extract_labels_fn: Callable[..., list[str]],
    dataset_config: "DatasetConfig",
) -> tuple[ModelOutput, list[dict | str | list[str]]]:
    """Evaluate a model on a single batch of examples through generation.

    Args:
        batch:
            The batch of examples to evaluate on.
        batch_idx:
            The index of the batch.
        batch_size:
            The size of the batch.
        non_cached_dataset:
            The dataset to evaluate on.
        model:
            The model to evaluate.
        tokenizer:
            The tokenizer used to encode the examples.
        stopping_criteria:
            The stopping criteria to use to stop generation.
        generation_config:
            The generation configuration to use.
        extract_labels_fn:
            The function to use to extract the labels from the model output.
        dataset_config:
            The configuration of the dataset.

    Returns:
        The predictions generated so far, with the predictions for the current batch
        appended.
    """
    # Generate the completions of the documents in the batch
    with torch.inference_mode():
        inputs = batch["input_ids"].to(model.device)
        stopping_criteria.clear()

        prefix_allowed_tokens_fn = None
        logits_processors = None
        if dataset_config.task == NER and isinstance(
            tokenizer, PreTrainedTokenizerBase
        ):
            ner_tag_names = list(dataset_config.prompt_label_mapping.values())
            prefix_allowed_tokens_fn = get_ner_prefix_allowed_tokens_fn(
                ner_tag_names=ner_tag_names, tokenizer=tokenizer
            )
            if isinstance(model, VLLMModel):
                logits_processors = get_ner_logits_processors(
                    ner_tag_names=ner_tag_names, llm=model
                )

        model_output = model.generate(
            inputs=inputs,
            attention_mask=batch["attention_mask"].to(model.device)
            if "attention_mask" in batch
            else None,
            generation_config=generation_config,
            stopping_criteria=StoppingCriteriaList([stopping_criteria]),
            prefix_allowed_tokens_fn=prefix_allowed_tokens_fn,
            logits_processors=logits_processors,
        )
        assert isinstance(model_output, ModelOutput)

    # Some models include the input in the generated sequence, so we need to remove the
    # input if it is present
    inputs = inputs.detach().cpu()
    model_output.sequences = model_output.sequences.detach().cpu()
    if torch.equal(model_output.sequences[:, : inputs.shape[1]], inputs):
        model_output.sequences = model_output.sequences[:, inputs.shape[1] :]

    # Extract the labels from the model output and store them for metric computation
    # later
    batch_start = batch_idx * batch_size
    batch_end = (batch_idx + 1) * batch_size
    input_batch = non_cached_dataset[batch_start:batch_end]
    extracted_labels: list = extract_labels_fn(
        input_batch=input_batch, model_output=model_output, tokenizer=tokenizer
    )

    return model_output, extracted_labels


def extract_raw_predictions(
    generated_sequences: torch.Tensor, tokenizer: "Tokenizer"
) -> list[str]:
    """Get the raw predictions from the generated sequences.

    Args:
        generated_sequences:
            The generated sequences from the model. The outer-most list is the
            batch dimension, the inner-most list is the sequence dimension,
            consisting of token IDs.
        tokenizer:
            The tokenizer used to generate the tokens.

    Returns:
        The candidate labels with the smallest edit distance to the predicted labels.
    """
    raw_predictions: list[str] = [
        tokenizer.decode(completion_ids.tolist(), skip_special_tokens=True).split(
            "\n\n"
        )[0]
        for completion_ids in generated_sequences.long()
    ]

    end_of_chat_token_ids = get_end_of_chat_token_ids(tokenizer=tokenizer)
    if end_of_chat_token_ids is not None:
        end_of_chat_token = tokenizer.decode(end_of_chat_token_ids).strip()
        if end_of_chat_token:
            raw_predictions = [
                raw_prediction.split(end_of_chat_token)[0]
                for raw_prediction in raw_predictions
            ]

    raw_predictions = [raw_prediction.strip() for raw_prediction in raw_predictions]

    return raw_predictions


def get_generation_stopping_criteria(
    tokenizer: "Tokenizer", model: "GenerativeModel"
) -> StopWordCriteria:
    """Get the stopping criteria for generation.

    Args:
        tokenizer:
            The tokenizer used to tokenize the stop words.
        model:
            The generative model, which we use to ensure the tensors are on the
            same device, and also determine whether stop words are needed, based on
            the model type.

    Returns:
        The stopping criteria for generation.
    """
    if isinstance(model, OpenAIModel):
        return StopWordCriteria(stop_word_id_lists=[])

    double_newline_ids: list[int] = tokenizer(
        text=["\n\n"], add_special_tokens=False
    ).input_ids[0]
    single_newline_ids: list[int] = tokenizer(
        text=["\n"], add_special_tokens=False
    ).input_ids[0]

    stop_word_id_lists = [double_newline_ids, single_newline_ids + single_newline_ids]

    end_chat_token_ids = get_end_of_chat_token_ids(tokenizer=tokenizer)
    if end_chat_token_ids is not None:
        stop_word_id_lists.append(end_chat_token_ids)

    if tokenizer.bos_token is not None:
        bos_token_ids: list[int] = tokenizer(
            text=[tokenizer.bos_token], add_special_tokens=False
        ).input_ids[0]
        stop_word_id_lists.append(bos_token_ids)

    if tokenizer.eos_token is not None:
        eos_token_ids: list[int] = tokenizer(
            text=[tokenizer.eos_token], add_special_tokens=False
        ).input_ids[0]
        stop_word_id_lists.append(eos_token_ids)

    def remove_empty_tokens(token_id_list: list[int]) -> list[int]:
        return [
            token_id for token_id in token_id_list if tokenizer.decode([token_id]) != ""
        ]

    stop_word_id_lists = [
        remove_empty_tokens(token_id_list) for token_id_list in stop_word_id_lists
    ]

    return StopWordCriteria(stop_word_id_lists=stop_word_id_lists)


def debug_log(
    batch_idx: int,
    batch_size: int,
    non_cached_dataset: Dataset,
    extracted_labels: list[dict | str | list[str]],
    dataset_config: "DatasetConfig",
) -> None:
    """Log inputs and outputs for debugging purposes.

    Args:
        batch_idx:
            The index of the batch.
        batch_size:
            The size of the batch.
        non_cached_dataset:
            The dataset to evaluate on.
        extracted_labels:
            The extracted labels from the model output.
        dataset_config:
            The configuration of the dataset.
    """
    sample_idxs = range(
        batch_idx * batch_size,
        min((batch_idx + 1) * batch_size, len(non_cached_dataset)),
    )
    samples = non_cached_dataset.select(sample_idxs)

    if dataset_config.task == NER:
        log_msgs = [""]
        for tokens, predictions, labels in zip(
            samples["tokens"], extracted_labels, samples["labels"]
        ):
            predictions = [tag.upper() for tag in predictions]
            sample = list(zip(tokens, predictions, labels))
            log_batches = [
                [("Tokens: ", "Predictions: ", "Labels: ")] + sample[i : i + 10]
                for i in range(0, len(sample), 10)
            ]
            for log_batch in log_batches:
                lengths = [len(max(triple, key=len)) for triple in log_batch]
                log_batch = [
                    [f"{x:<{length}}" for x in triple]
                    for triple, length in zip(log_batch, lengths)
                ]
                tokens = [triple[0] for triple in log_batch]
                predictions = [triple[1] for triple in log_batch]
                labels = [triple[2] for triple in log_batch]
                log_msgs.append(
                    "\t".join(tokens)
                    + "\n"
                    + "\t".join(predictions)
                    + "\n"
                    + "\t".join(labels)
                )
        logger.info("\n\n".join(log_msgs))

    else:
        # Define predictions
        if dataset_config.task == RC:
            extracted_labels = [
                prediction["prediction_text"]
                for prediction in extracted_labels
                if isinstance(prediction, dict)
            ]

        # Define labels
        if dataset_config.task in {SENT, LA}:
            labels = [
                dataset_config.prompt_label_mapping.get(label, label).lower()
                for label in samples["label"]
            ]
        elif dataset_config.task == RC:
            labels = [label["answers"]["text"][0] for label in samples["label"]]
        elif dataset_config.task == SUMM:
            labels = samples["target_text"]
        else:
            labels = samples["label"]

        # Log inputs and outputs
        for input_text, prediction, label in zip(
            samples["text"], extracted_labels, labels
        ):
            logger.info(
                f"Input: '{input_text}'\n"
                f"Prediction: '{prediction}'\n"
                f"Label: '{label}'"
            )
