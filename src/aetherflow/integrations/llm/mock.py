"""Fully deterministic mock LLM for testing and demos."""

from __future__ import annotations
from typing import Any, Optional
from aetherflow.integrations.llm.base import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    async def complete(self, messages: list[dict[str, str]], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048, **kwargs: Any) -> dict[str, Any]:
        last = messages[-1]["content"] if messages else ""
        return {"content": f"Mock response to: {last[:100]}", "model": "mock-llm", "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        return [[0.1] * 8 for _ in texts]
