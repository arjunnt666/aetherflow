"""OpenAI chat completions over plain HTTP (works with any compatible endpoint)."""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx

from aetherflow.integrations.llm.base import BaseLLMClient


def _plain(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    # the tool loop emits {"role": "tool"} without call ids; send those as user text
    out = []
    for m in messages:
        if m.get("role") == "tool":
            out.append({"role": "user", "content": f"[{m.get('name', 'tool')} result] {m['content']}"})
        else:
            out.append({"role": m["role"], "content": m["content"]})
    return out


class OpenAIClient(BaseLLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "gpt-4o",
        timeout: float = 120.0,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAIClient needs api_key or OPENAI_API_KEY")
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self.model = model
        self._http = httpx.AsyncClient(
            timeout=timeout, headers={"Authorization": f"Bearer {self.api_key}"}
        )

    async def complete(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> dict[str, Any]:
        model = model or self.model
        r = await self._http.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model,
                "messages": _plain(messages),
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs,
            },
        )
        r.raise_for_status()
        data = r.json()
        return {
            "content": data["choices"][0]["message"].get("content") or "",
            "tool_calls": [],
            "model": data.get("model", model),
            "usage": data.get("usage", {}),
        }

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        r = await self._http.post(
            f"{self.base_url}/embeddings",
            json={"model": model or "text-embedding-3-small", "input": texts},
        )
        r.raise_for_status()
        return [d["embedding"] for d in sorted(r.json()["data"], key=lambda d: d["index"])]
