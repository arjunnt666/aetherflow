"""OpenAI-compatible LLM client (hollow / requires API key)."""

from __future__ import annotations
import logging
from typing import Any, Optional
from aetherflow.integrations.llm.base import BaseLLMClient

logger = logging.getLogger("aetherflow.llm.openai")


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"

    async def complete(self, messages: list[dict[str, str]], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048, **kwargs: Any) -> dict[str, Any]:
        logger.warning("OpenAIClient.complete called in simulation mode")
        return {"content": "[Simulated OpenAI response — configure OPENAI_API_KEY for real calls]", "model": model or "gpt-4o", "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}}

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]
