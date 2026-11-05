"""Anthropic Messages API over plain HTTP."""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx

from aetherflow.integrations.llm.base import BaseLLMClient
from aetherflow.integrations.llm.openai_client import _plain


class AnthropicClient(BaseLLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5",
        base_url: str = "https://api.anthropic.com/v1",
        timeout: float = 120.0,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("AnthropicClient needs api_key or ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._http = httpx.AsyncClient(
            timeout=timeout,
            headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
        )

    async def complete(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> dict[str, Any]:
        msgs = _plain(messages)
        system = "\n".join(m["content"] for m in msgs if m["role"] == "system")
        body: dict[str, Any] = {
            "model": model or self.model,
            "messages": [m for m in msgs if m["role"] != "system"],
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }
        if system:
            body["system"] = system
        r = await self._http.post(f"{self.base_url}/messages", json=body)
        r.raise_for_status()
        data = r.json()
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        return {
            "content": text,
            "tool_calls": [],
            "model": data.get("model", body["model"]),
            "usage": data.get("usage", {}),
        }

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        raise NotImplementedError("Anthropic has no embeddings endpoint; use OpenAIClient.embed")
