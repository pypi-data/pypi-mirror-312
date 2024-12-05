"""Utility functions related to structured generation."""

import importlib.util
from typing import TYPE_CHECKING, Any, Callable

import torch
from pydantic import BaseModel, conlist, create_model

if importlib.util.find_spec("outlines") is not None:
    from outlines.integrations.transformers import JSONPrefixAllowedTokens
    from outlines.integrations.vllm import JSONLogitsProcessor

if TYPE_CHECKING:
    from outlines.integrations.transformers import JSONPrefixAllowedTokens
    from transformers import PreTrainedTokenizerBase
    from vllm import LLM


def get_ner_schema(ner_tag_names: list[str]) -> type[BaseModel]:
    """Get the schema for the NER answer format, used for structured generation.

    Args:
        ner_tag_names:
            The NER tag names.

    Returns:
        The schema for the NER answer format.
    """
    keys_and_their_types: dict[str, Any] = {
        tag_name: (conlist(str, max_length=5), ...) for tag_name in ner_tag_names
    }
    schema = create_model("AnswerFormat", **keys_and_their_types)
    return schema


def get_ner_prefix_allowed_tokens_fn(
    ner_tag_names: list[str], tokenizer: "PreTrainedTokenizerBase"
) -> "JSONPrefixAllowedTokens":
    """Get the prefix allowed tokens function for the NER task, used in `transformers`.

    Args:
        ner_tag_names:
            The NER tag names.
        tokenizer:
            The tokenizer to use for tokenizing the JSON Schema.

    Returns:
        The prefix allowed tokens function for the NER task.
    """
    return JSONPrefixAllowedTokens(
        schema=get_ner_schema(ner_tag_names=ner_tag_names),
        tokenizer_or_pipe=tokenizer,
        whitespace_pattern=r" ?",
    )


def get_ner_logits_processors(
    ner_tag_names: list[str], llm: "LLM"
) -> list[Callable[[list[int], torch.Tensor], torch.Tensor]]:
    """Get the logits processors for the NER task, used in vLLM.

    Args:
        ner_tag_names:
            The NER tag names.
        llm:
            The vLLM model.

    Returns:
        The logit processors for the NER task.
    """
    logits_processor = JSONLogitsProcessor(
        schema=get_ner_schema(ner_tag_names=ner_tag_names),
        llm=llm,
        whitespace_pattern=r" ?",
    )
    return [logits_processor]
