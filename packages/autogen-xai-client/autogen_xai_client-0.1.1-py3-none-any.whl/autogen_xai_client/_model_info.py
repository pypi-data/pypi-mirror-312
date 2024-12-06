from typing import Dict

from autogen_core.components.models import ModelCapabilities

# Based on: https://platform.openai.com/docs/models/continuous-model-upgrades
# This is a moving target, so correctness is checked by the model value returned by openai against expected values at runtime``
_MODEL_POINTERS = {
    "grok-beta": "grok-beta",
    "grok-vision-beta": "grok-vision-beta",
}

_MODEL_CAPABILITIES: Dict[str, ModelCapabilities] = {
    "grok-beta": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
    },
    "grok-vision-beta": {
        "vision": True,
        "function_calling": True,
        "json_output": True,
    },
}

_MODEL_TOKEN_LIMITS: Dict[str, int] = {
    "grok-beta": 131072,
    "grok-vision-beta": 8192,
}


def resolve_model(model: str) -> str:
    if model in _MODEL_POINTERS:
        return _MODEL_POINTERS[model]
    return model


def get_capabilities(model: str) -> ModelCapabilities:
    resolved_model = resolve_model(model)
    return _MODEL_CAPABILITIES[resolved_model]


def get_token_limit(model: str) -> int:
    resolved_model = resolve_model(model)
    return _MODEL_TOKEN_LIMITS[resolved_model]
