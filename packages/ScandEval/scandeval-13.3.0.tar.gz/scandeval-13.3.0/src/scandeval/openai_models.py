"""Model and tokenizer wrapper for OpenAI models."""

import importlib.util
import logging
import math
from typing import TYPE_CHECKING, Literal

import torch
from torch import LongTensor
from torch.nn.utils.rnn import pad_sequence
from transformers import BatchEncoding, GenerationConfig
from transformers.modeling_utils import ModelOutput

from .config import BenchmarkConfig, DatasetConfig, ModelConfig
from .exceptions import InvalidBenchmark, InvalidModel, NeedsExtraInstalled
from .tasks import NER
from .types import is_list_of_int, is_list_of_list_of_int

if TYPE_CHECKING:
    import tiktoken
    from torch import Tensor
    from transformers import PretrainedConfig

if importlib.util.find_spec("tiktoken") is not None:
    import tiktoken

if importlib.util.find_spec("openai") is not None:
    from openai import AzureOpenAI, BadRequestError, NotFoundError, OpenAI
    from openai.types.chat import ChatCompletionUserMessageParam
    from openai.types.chat.chat_completion_token_logprob import TopLogprob
    from openai.types.shared.response_format_json_object import ResponseFormatJSONObject

logger = logging.getLogger(__package__)


class OpenAITokenizer:
    """An OpenAI tokenizer.

    Attributes:
        model_config:
            The model configuration.
        hf_model_config:
            The Hugging Face model configuration.
        encoding:
            The encoding.
    """

    unk_token: str | None = "<unk>"
    unk_token_id = -1
    pad_token: str | None = "<pad>"
    padding_side: Literal["right", "left"] = "left"
    is_fast = False
    chat_template: str | None = None

    def __init__(
        self, model_config: ModelConfig, hf_model_config: "PretrainedConfig"
    ) -> None:
        """Initialize the tokenizer.

        Args:
            model_config:
                The model configuration.
            hf_model_config:
                The Hugging Face model configuration.
        """
        self.model_config = model_config
        self.hf_model_config = hf_model_config
        self.model_max_length = self.hf_model_config.model_max_length

        self.bos_token_id: int = self.hf_model_config.bos_token_id or -1
        self.cls_token_id: int = self.bos_token_id
        self.eos_token_id: int = self.hf_model_config.eos_token_id or -1
        self.sep_token_id: int = self.eos_token_id
        self.pad_token_id: int = self.hf_model_config.pad_token_id or -1

        self.bos_token: str | None = self.encoding.decode([self.bos_token_id])
        self.cls_token: str | None = self.bos_token
        self.eos_token: str | None = self.encoding.decode([self.eos_token_id])
        self.sep_token: str | None = self.eos_token

        assert self.bos_token is not None
        assert self.cls_token is not None
        assert self.eos_token is not None
        assert self.sep_token is not None
        assert self.pad_token is not None

        self.vocab_size = self.encoding.max_token_value + 1
        self.special_tokens_map: dict[str, str] = dict(
            bos_token=self.bos_token,
            cls_token=self.cls_token,
            eos_token=self.eos_token,
            sep_token=self.sep_token,
            pad_token=self.pad_token,
        )

    @property
    def encoding(self) -> "tiktoken.Encoding":
        """Return the underlying tiktoken encoding."""
        try:
            return tiktoken.encoding_for_model(model_name=self.model_config.model_id)
        except KeyError:
            # For Azure, the model_id is the deployment name. I do not know how to
            # dynamically get the currently deployed model so assuming Azure only
            # supports the latest models.
            # TODO: This needs to be fixed, as gpt-4o uses a different encoding
            return tiktoken.get_encoding("cl100k_base")

    def __call__(self, text: str | list[str], **kwargs) -> BatchEncoding:
        """Tokenize text.

        Args:
            text:
                The text to tokenize.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The tokenized text.
        """
        truncation = kwargs.get("truncation", False)
        start_idx = -self.model_max_length if truncation else 0

        text_list = [text] if isinstance(text, str) else text
        encoded_inputs = [
            BatchEncoding(
                dict(
                    input_ids=self.encoding.encode(
                        text,
                        allowed_special={
                            self.bos_token,
                            self.eos_token,
                            self.cls_token,
                            self.sep_token,
                            self.pad_token,
                        },
                    )[start_idx:]
                )
            )
            for text in text_list
        ]
        return self.pad(encoded_inputs=encoded_inputs)

    def decode(self, token_ids: list[int], **kwargs) -> str:
        """Decode token IDs.

        Args:
            token_ids:
                The token IDs to decode.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The decoded text.
        """
        token_ids = [
            token_id for token_id in token_ids if token_id != self.pad_token_id
        ]
        return self.encoding.decode(tokens=token_ids)

    def batch_decode(self, sequences: list[list[int]], **kwargs) -> list[str]:
        """Decode batched token IDs.

        Args:
            sequences:
                The token IDs to decode.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The decoded text.
        """
        return [self.decode(token_ids=sequence) for sequence in sequences]

    def encode(self, text: str, **kwargs) -> list[int]:
        """Encode text.

        Args:
            text:
                The text to encode.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The encoded text.
        """
        return self(text, **kwargs).input_ids.tolist()[0]

    def convert_ids_to_tokens(
        self, ids: int | list[int], skip_special_tokens: bool = False
    ) -> str | list[str]:
        """Convert token IDs to tokens.

        Args:
            ids:
                The token IDs to convert.
            skip_special_tokens:
                Whether to skip special tokens. Defaults to False.

        Returns:
            The tokens.
        """
        ids_list = [ids] if isinstance(ids, int) else ids
        tokens = [self.decode(token_ids=[i]) for i in ids_list]
        if skip_special_tokens:
            tokens = [
                token
                for token in tokens
                if token not in self.special_tokens_map.values()
            ]
        if len(tokens) == 1:
            return tokens[0]
        return tokens

    def convert_tokens_to_ids(self, tokens: str | list[str]) -> int | list[int]:
        """Convert tokens to token IDs.

        Args:
            tokens:
                The tokens to convert.

        Returns:
            The token IDs.
        """
        if isinstance(tokens, str):
            tokens = [tokens]
        ids = [self.encode(text=token)[0] for token in tokens]
        if len(ids) == 1:
            return ids[0]
        return ids

    def pad(
        self,
        encoded_inputs: (
            BatchEncoding
            | list[BatchEncoding]
            | dict[str, list[int]]
            | dict[str, list[list[int]]]
            | list[dict[str, list[int]]]
        ),
        **kwargs,
    ) -> BatchEncoding:
        """Pad encoded inputs.

        Args:
            encoded_inputs:
                Tokenized inputs. Can represent one input (BatchEncoding or Dict[str,
                List[int]]) or a batch of tokenized inputs (list of BatchEncoding,
                Dict[str, List[List[int]]] or List[Dict[str, List[int]]]) so you can
                use this method during preprocessing as well as in a PyTorch Dataloader
                collate function.
            **kwargs:
                Additional keyword arguments.
        """
        # Single example
        if isinstance(encoded_inputs, BatchEncoding):
            return encoded_inputs
        elif isinstance(encoded_inputs, dict) and is_list_of_int(
            encoded_inputs["input_ids"]
        ):
            return BatchEncoding(data=encoded_inputs)

        # Batch of examples
        if isinstance(encoded_inputs, dict) and is_list_of_list_of_int(
            encoded_inputs["input_ids"]
        ):
            input_ids = encoded_inputs["input_ids"]
        else:
            assert isinstance(encoded_inputs, list)
            input_ids = [list(example["input_ids"]) for example in encoded_inputs]

        # Flip the token IDs in the lists, since `pad_sequence` pads to the right by
        # default, and we want padding to the left
        flipped_input_ids: list["Tensor"] = []
        for input_id_list in input_ids:
            input_id_list.reverse()
            flipped_input_ids.append(LongTensor(input_id_list))

        padded_input_ids = (
            pad_sequence(
                sequences=flipped_input_ids,
                batch_first=True,
                padding_value=self.pad_token_id,
            )
            .flip(dims=[1])
            .long()
        )

        return BatchEncoding(dict(input_ids=padded_input_ids))

    def apply_chat_template(
        self, conversation: list[dict[Literal["role", "content"], str]], **kwargs
    ) -> str | list[int]:
        """Apply a chat template to a conversation.

        Args:
            conversation:
                The conversation to apply the chat template to.
            **kwargs:
                Additional keyword arguments.

        Returns:
            The chat template.
        """
        raise NotImplementedError("Chat templates are not supported for OpenAI models.")


class OpenAIModel:
    """An OpenAI model.

    Attributes:
        model_config:
            The model configuration.
        config:
            The Hugging Face model configuration.
        dataset_config:
            The dataset configuration.
        benchmark_config:
            The benchmark configuration.
        tokenizer:
            The tokenizer.
        device:
            The device to use, is always CPU.
        is_chat_model:
            Whether the model is a chat model.
    """

    def __init__(
        self,
        model_config: ModelConfig,
        hf_model_config: "PretrainedConfig",
        dataset_config: DatasetConfig,
        benchmark_config: BenchmarkConfig,
        tokenizer: OpenAITokenizer,
    ) -> None:
        """Initialize the model.

        Args:
            model_config:
                The model configuration.
            hf_model_config:
                The Hugging Face model configuration.
            dataset_config:
                The dataset configuration.
            benchmark_config:
                The benchmark configuration.
            tokenizer:
                The tokenizer.
        """
        if importlib.util.find_spec("openai") is None:
            raise NeedsExtraInstalled(extra="openai")

        self.model_config = model_config
        self.config = hf_model_config
        self.dataset_config = dataset_config
        self.benchmark_config = benchmark_config
        self.tokenizer = tokenizer
        self.device = torch.device("cpu")
        self.client = self._initialize_openai_client()
        self.is_chat_model = self._is_chat_model()
        self.supports_json_mode = self._supports_json_mode()

    def _initialize_openai_client(self) -> "OpenAI | AzureOpenAI":
        """Initialize and return the OpenAI client.

        Returns:
            The OpenAI client.

        Raises:
            InvalidBenchmark:
                If the OpenAI API key is not specified.
        """
        if self.benchmark_config.openai_api_key is not None:
            return OpenAI(api_key=self.benchmark_config.openai_api_key, max_retries=60)
        elif self.benchmark_config.azure_openai_api_key is not None:
            if (
                self.benchmark_config.azure_openai_endpoint is None
                or self.benchmark_config.azure_openai_api_version is None
            ):
                if self.benchmark_config.run_with_cli:
                    argument_message = (
                        "`--azure-openai-endpoint` and `--azure_openai_api_version` "
                        "flags"
                    )
                else:
                    argument_message = (
                        "`azure_openai_endpoint` and `azure_openai_api_version` "
                        "arguments in the `Benchmarker` class"
                    )
                raise InvalidModel(
                    "Azure OpenAI models require an endpoint and API version to be "
                    "specified. Please specify the endpoint with the "
                    f"{argument_message}, or specify the environment variables "
                    "`AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_VERSION`."
                )
            return AzureOpenAI(
                api_key=self.benchmark_config.azure_openai_api_key,
                azure_endpoint=self.benchmark_config.azure_openai_endpoint,
                api_version=self.benchmark_config.azure_openai_api_version,
                max_retries=60,
            )
        elif self.benchmark_config.run_with_cli:
            raise InvalidModel(
                "OpenAI models require an API key to be specified. Please specify the "
                "`--openai-api-key` argument (or `--azure-openai-api-key` and "
                "`--azure-openai-endpoint` arguments) or specify the environment "
                "variables `OPENAI_API_KEY` (or `AZURE_OPENAI_API_KEY` and "
                "`AZURE_OPENAI_ENDPOINT`)."
            )
        else:
            raise InvalidModel(
                "OpenAI models require an API key to be specified. Please specify the "
                "`openai_api_key` argument to the `Benchmarker` class (or "
                "`azure_openai_api_key` and `azure_openai_endpoint` arguments) or "
                "specify the environment variables `OPENAI_API_KEY` (or "
                "`AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT`)."
            )

    def _is_chat_model(self) -> bool:
        """Returns whether the model is a chat model."""
        try:
            self.client.completions.create(
                model=self.model_config.model_id, prompt="Test", max_tokens=1
            )
            return False
        except (NotFoundError, BadRequestError) as e:
            chat_model_strings = [
                "This is a chat model",
                "The completion operation does not work with the specified model",
            ]
            if any(string in str(e) for string in chat_model_strings):
                return True
            raise e

    def _supports_json_mode(self) -> bool:
        """Returns whether the model supports JSON mode."""
        if not self.is_chat_model:
            return False

        try:
            self.client.chat.completions.create(  # type: ignore[call-overload]
                model=self.model_config.model_id,
                messages=[
                    ChatCompletionUserMessageParam(role="user", content="Test json")
                ],
                max_tokens=1,
                response_format=ResponseFormatJSONObject(type="json_object"),
            )
            return True
        except BadRequestError as e:
            no_json_mode_strings = ["not supported with this model"]
            if any(string in str(e) for string in no_json_mode_strings):
                return False
            raise e

    def generate(
        self,
        inputs: "Tensor",
        generation_config: GenerationConfig | None = None,
        **generation_kwargs,
    ) -> "Tensor | LongTensor | ModelOutput":
        """Generate text using the model.

        Args:
            inputs:
                The input IDs, of shape (batch_size, sequence_length).
            generation_config:
                The generation configuration. If None then a default GenerationConfig
                will be used. Defaults to None.
            **generation_kwargs:
                Additional keyword arguments. Can also be used to override
                generation configuration.

        Returns:
            The model output.
        """
        if generation_config is None:
            generation_config = GenerationConfig(**generation_kwargs)
        else:
            for key, value in generation_kwargs.items():
                setattr(generation_config, key, value)

        multiple_inputs = inputs.size(dim=0) > 1
        if multiple_inputs:
            raise ValueError(
                "OpenAI models do not support multiple inputs. Please use a batch "
                "size of 1."
            )

        two_dimensional_input = len(inputs.size()) == 2
        if two_dimensional_input:
            inputs = inputs[0]

        prompt = self.tokenizer.decode(
            [
                token_id
                for token_id in inputs.tolist()
                if token_id != self.config.pad_token_id
            ]
        )

        model_id = self.model_config.model_id
        max_tokens: int = generation_config.max_new_tokens or 1
        temperature = (
            0.0 if not generation_config.do_sample else generation_config.temperature
        )
        generation_kwargs = dict(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=generation_config.top_p,
            n=generation_config.num_return_sequences,
            frequency_penalty=generation_config.repetition_penalty - 1.0,
            stop=["\n\n", self.tokenizer.eos_token, self.tokenizer.pad_token],
            seed=4242,
        )

        if generation_config.output_scores:
            generation_kwargs["logprobs"] = True
            generation_kwargs["top_logprobs"] = 10

        if (
            self.dataset_config.task == NER
            and self.supports_json_mode
            and "json" in prompt.lower()
        ):
            generation_kwargs["response_format"] = dict(type="json_object")

        try:
            if not self.is_chat_model:
                model_output = self.client.completions.create(
                    prompt=prompt, **generation_kwargs
                )
                generation_output = model_output.choices[0].text.strip()
            else:
                model_output = self.client.chat.completions.create(
                    messages=[dict(role="system", content=prompt)], **generation_kwargs
                )
                generation_output = model_output.choices[0].message.content.strip()
        except BadRequestError as e:
            raise InvalidBenchmark(
                f"Encountered error during OpenAI generation: {str(e)!r}\n"
                f"The prompt causing it was {prompt!r}."
            )

        completion_ids = self.tokenizer([generation_output]).input_ids.tolist()
        output = LongTensor(completion_ids)

        if generation_config.return_dict_in_generate:
            output_dict: dict[str, Tensor | tuple] = dict(sequences=output)

            # Add logprobs scores to the output
            if generation_config.output_scores:
                # Create a list with placeholder logprobs for every token generated.
                # Each tensor in the list will be of shape (batch_size, vocab_size)
                batch_size = 1
                vocab_size = self.config.vocab_size
                logprobs_list = model_output.choices[0].logprobs.content
                seq_len = len(logprobs_list)
                scores = [
                    torch.full(size=(batch_size, vocab_size), fill_value=-math.inf)
                    for _ in range(seq_len)
                ]

                # Fill in the logprobs for each generated token. The logprobs from the
                # OpenAI output only contain the logprobs for the top-k tokens, so we
                # only fill in these and leave the rest at ~0% probability
                for gen_token_idx, logprobs in enumerate(logprobs_list):
                    # Remove duplicate logprobs, since, e.g., "negative" and " negative"
                    # can both be included in the list, and we only want the one with
                    # the highest logprob
                    top_logprobs: list[TopLogprob] = list()
                    for logprob_obj in logprobs.top_logprobs:
                        token = logprob_obj.token.strip()
                        if token in {lg.token.strip() for lg in top_logprobs}:
                            continue
                        top_logprobs.append(logprob_obj)

                    for logprob_obj in top_logprobs:
                        logprob = logprob_obj.logprob
                        token = logprob_obj.token.strip()
                        if token:
                            token_idx = self.tokenizer.encode(text=token)[0]
                            scores[gen_token_idx][0, token_idx] = logprob

                output_dict["scores"] = tuple(scores)

            return ModelOutput(output_dict)

        return output

    def to(self, device: torch.device) -> "OpenAIModel":
        """Move the model to a device.

        Args:
            device:
                The device to move the model to.

        Returns:
            The model.
        """
        return self

    def eval(self) -> "OpenAIModel":
        """Put the model in evaluation mode.

        Returns:
            The model.
        """
        return self

    def __call__(self, *args, **kwargs):
        """Call the model."""
        raise NotImplementedError("OpenAI models do not support the `__call__` method.")
