import os

from aetherflow.integrations.llm.base import BaseLLMClient
from aetherflow.integrations.llm.openai_client import OpenAIClient
from aetherflow.integrations.llm.anthropic_client import AnthropicClient
from aetherflow.integrations.llm.mock import MockLLMClient


def make_client(cfg=None) -> BaseLLMClient:
    """Pick a client from LLMConfig. Falls back to the mock when no key is set,
    so tests and the demo run offline."""
    provider = getattr(cfg, "provider", "openai")
    key = getattr(cfg, "api_key", None)
    model = getattr(cfg, "model", None)
    if provider == "anthropic" and (key or os.environ.get("ANTHROPIC_API_KEY")):
        return AnthropicClient(api_key=key, **({"model": model} if model else {}))
    if provider == "openai" and (key or os.environ.get("OPENAI_API_KEY")):
        return OpenAIClient(
            api_key=key, base_url=getattr(cfg, "base_url", None), model=model or "gpt-4o"
        )
    return MockLLMClient()


__all__ = ["BaseLLMClient", "OpenAIClient", "AnthropicClient", "MockLLMClient", "make_client"]
