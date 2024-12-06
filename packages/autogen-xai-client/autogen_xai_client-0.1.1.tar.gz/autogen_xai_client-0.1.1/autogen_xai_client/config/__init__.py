from typing import Dict, List, Literal, Optional, Union

from autogen_core.components.models import ModelCapabilities
from typing_extensions import TypedDict


class ResponseFormat(TypedDict):
    type: Literal["text", "json_object"]


class CreateArguments(TypedDict, total=False):
    frequency_penalty: Optional[float]
    logit_bias: Optional[Dict[str, int]]
    max_tokens: Optional[int]
    n: Optional[int]
    presence_penalty: Optional[float]
    response_format: ResponseFormat
    seed: Optional[int]
    stop: Union[Optional[str], List[str]]
    temperature: Optional[float]
    top_p: Optional[float]
    user: str


class BaseOpenAIClientConfiguration(CreateArguments, total=False):
    model: str
    api_key: str
    timeout: Union[float, None]
    max_retries: int
    model_capabilities: ModelCapabilities
    """What functionality the model supports, determined by default from model name but is overriden if value passed."""


class XAIClientConfiguration(BaseOpenAIClientConfiguration, total=False):
    base_url: str
    # Not required
    model_capabilities: ModelCapabilities


__all__ = [
    "XAIClientConfiguration",
]
