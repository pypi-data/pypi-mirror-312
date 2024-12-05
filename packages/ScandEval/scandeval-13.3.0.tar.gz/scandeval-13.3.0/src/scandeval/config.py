"""Configuration classes used throughout the project."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

import torch

if TYPE_CHECKING:
    from .enums import Framework, ModelType


@dataclass
class MetricConfig:
    """Configuration for a metric.

    Attributes:
        name:
            The name of the metric.
        pretty_name:
            A longer prettier name for the metric, which allows cases and spaces. Used
            for logging.
        huggingface_id:
            The Hugging Face ID of the metric.
        results_key:
            The name of the key used to extract the metric scores from the results
            dictionary.
        compute_kwargs:
            Keyword arguments to pass to the metric's compute function. Defaults to
            an empty dictionary.
        postprocessing_fn:
            A function to apply to the metric scores after they are computed, taking
            the score to the postprocessed score along with its string representation.
            Defaults to x -> (100 * x, f"{x:.2%}").
    """

    name: str
    pretty_name: str
    huggingface_id: str
    results_key: str
    compute_kwargs: dict[str, Any] = field(default_factory=dict)
    postprocessing_fn: Callable[[float], tuple[float, str]] = field(
        default_factory=lambda: lambda raw_score: (100 * raw_score, f"{raw_score:.2%}")
    )

    def __hash__(self) -> int:
        """Return a hash of the metric configuration."""
        return hash(self.name)


@dataclass
class Task:
    """A dataset task.

    Attributes:
        name:
            The name of the task.
        supertask:
            The supertask of the task, describing the overall type of task.
        metrics:
            The metrics used to evaluate the task.
        labels:
            The labels used in the task.
    """

    name: str
    supertask: str
    metrics: list[MetricConfig]
    labels: list[str]

    def __hash__(self) -> int:
        """Return a hash of the task."""
        return hash(self.name)


@dataclass
class Language:
    """A benchmarkable language.

    Attributes:
        code:
            The ISO 639-1 language code of the language.
        name:
            The name of the language.
    """

    code: str
    name: str

    def __hash__(self) -> int:
        """Return a hash of the language."""
        return hash(self.code)


@dataclass
class BenchmarkConfig:
    """General benchmarking configuration, across datasets and models.

    Attributes:
        model_languages:
            The languages of the models to benchmark.
        dataset_languages:
            The languages of the datasets in the benchmark.
        tasks:
            The tasks benchmark the model(s) on.
        datasets:
            The datasets to benchmark on.
        framework:
            The framework of the models to benchmark. If None then the framework will be
            inferred.
        batch_size:
            The batch size to use.
        raise_errors:
            Whether to raise errors instead of skipping them.
        cache_dir:
            Directory to store cached models and datasets.
        evaluate_train:
            Whether to evaluate on the training set.
        token:
            The authentication token for the Hugging Face Hub. If a boolean value is
            specified then the token will be fetched from the Hugging Face CLI, where
            the user has logged in through `huggingface-cli login`. If a string is
            specified then it will be used as the token.
        openai_api_key:
            The API key for the OpenAI API. If None then OpenAI models will not be
            benchmarked.
        azure_openai_api_key:
            The API key for the Azure OpenAI API. If None then Azure OpenAI models will
            not be benchmarked.
        azure_openai_endpoint:
            The endpoint for the Azure OpenAI API. If None then Azure OpenAI models will
            not be benchmarked.
        azure_openai_api_version:
            The api version for the Azure OpenAI API, e.g. "2023-12-01-preview". If
            None then Azure OpenAI models will not be benchmarked.
        force:
            Whether to force the benchmark to run even if the results are already
            cached.
        progress_bar:
            Whether to show a progress bar.
        save_results:
            Whether to save the benchmark results to 'scandeval_benchmark_results.json'.
        device:
            The device to use for benchmarking.
        verbose:
            Whether to print verbose output.
        trust_remote_code:
            Whether to trust remote code when loading models from the Hugging Face Hub.
        load_in_4bit:
            Whether to load models in 4-bit precision. If None then this will be done
            if CUDA is available and the model is a decoder model.
        use_flash_attention:
            Whether to use Flash Attention. If None then this will be used for
            generative models.
        clear_model_cache:
            Whether to clear the model cache after benchmarking each model.
        only_validation_split:
            Whether to only evaluate on the validation split.
        few_shot:
            Whether to only evaluate the model using few-shot evaluation. Only relevant
            if the model is generative.
        num_iterations:
            The number of iterations each model should be evaluated for.
        debug:
            Whether to run the benchmark in debug mode.
        run_with_cli:
            Whether the benchmark is being run with the CLI.
    """

    model_languages: list[Language]
    dataset_languages: list[Language]
    tasks: list[Task]
    datasets: list[str]
    framework: "Framework | None"
    batch_size: int
    raise_errors: bool
    cache_dir: str
    evaluate_train: bool
    token: bool | str | None
    openai_api_key: str | None
    azure_openai_api_key: str | None
    azure_openai_endpoint: str | None
    azure_openai_api_version: str | None
    force: bool
    progress_bar: bool
    save_results: bool
    device: torch.device
    verbose: bool
    trust_remote_code: bool
    load_in_4bit: bool | None
    use_flash_attention: bool | None
    clear_model_cache: bool
    only_validation_split: bool
    few_shot: bool
    num_iterations: int
    debug: bool
    run_with_cli: bool


@dataclass
class DatasetConfig:
    """Configuration for a dataset.

    Attributes:
        name:
            The name of the dataset. Must be lower case with no spaces.
        pretty_name:
            A longer prettier name for the dataset, which allows cases and spaces. Used
            for logging.
        huggingface_id:
            The Hugging Face ID of the dataset.
        task:
            The task of the dataset.
        languages:
            The ISO 639-1 language codes of the entries in the dataset.
        id2label:
            The mapping from ID to label.
        label2id:
            The mapping from label to ID.
        num_labels:
            The number of labels in the dataset.
        prompt_template:
            The template for the prompt to use when benchmarking the dataset using
            few-shot evaluation.
        max_generated_tokens:
            The maximum number of tokens to generate when benchmarking the dataset
            using few-shot evaluation.
        prompt_prefix:
            The prefix to use in the few-shot prompt.
        num_few_shot_examples:
            The number of examples to use when benchmarking the dataset using few-shot
            evaluation. For a classification task, these will be drawn evenly from
            each label.
        instruction_prompt:
            The prompt to use when benchmarking the dataset using instruction-based
            evaluation.
        prompt_label_mapping (optional):
            A mapping from the labels to another phrase which is used as a substitute
            for the label in few-shot evaluation. Defaults to an empty dictionary.
        unofficial (optional):
            Whether the dataset is unofficial. Defaults to False.
    """

    name: str
    pretty_name: str
    huggingface_id: str
    task: Task
    languages: list[Language]
    prompt_template: str
    max_generated_tokens: int
    prompt_prefix: str
    num_few_shot_examples: int
    instruction_prompt: str
    prompt_label_mapping: dict[str, str] = field(default_factory=dict)
    unofficial: bool = False

    @property
    def id2label(self) -> dict[int, str]:
        """The mapping from ID to label."""
        return {idx: label for idx, label in enumerate(self.task.labels)}

    @property
    def label2id(self) -> dict[str, int]:
        """The mapping from label to ID."""
        return {label: i for i, label in enumerate(self.task.labels)}

    @property
    def num_labels(self) -> int:
        """The number of labels in the dataset."""
        return len(self.task.labels)

    def __hash__(self) -> int:
        """Return a hash of the dataset configuration."""
        return hash(self.name)


@dataclass
class ModelConfig:
    """Configuration for a model.

    Attributes:
        model_id:
            The ID of the model.
        revision:
            The revision of the model.
        framework:
            The framework of the model.
        task:
            The task that the model was trained on.
        languages:
            The languages of the model.
        model_type:
            The type of the model.
        model_cache_dir:
            The directory to cache the model in.
        adapter_base_model_id:
            The model ID of the base model if the model is an adapter model. Can be None
            if the model is not an adapter model.
    """

    model_id: str
    revision: str
    framework: "Framework"
    task: str
    languages: list[Language]
    model_type: "ModelType | str"
    model_cache_dir: str
    adapter_base_model_id: str | None

    def __hash__(self) -> int:
        """Return a hash of the model configuration."""
        return hash(self.model_id)
