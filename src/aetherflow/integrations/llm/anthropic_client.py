"""Anthropic Claude client (hollow)."""

from __future__ import annotations
import logging
from typing import Any, Optional
from aetherflow.integrations.llm.base import BaseLLMClient

logger = logging.getLogger("aetherflow.llm.anthropic")


class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def complete(self, messages: list[dict[str, str]], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048, **kwargs: Any) -> dict[str, Any]:
        logger.warning("AnthropicClient.complete called in simulation mode")
        return {"content": "[Simulated Anthropic response — configure ANTHROPIC_API_KEY for real calls]", "model": model or "claude-3-5-sonnet-20241022", "usage": {"input_tokens": 0, "output_tokens": 0}}

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        return [[0.0] * 1024 for _ in texts]
