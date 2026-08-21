"""Fully deterministic mock LLM for testing and demos."""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from aetherflow.integrations.llm.base import BaseLLMClient

# Pull a calculator-safe expression out of a sentence.
_EXPR = re.compile(r"([0-9]+(?:\s*[+\-*/%()]\s*[0-9]+)+)")


class MockLLMClient(BaseLLMClient):
    async def complete(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> dict[str, Any]:
        last = messages[-1] if messages else {}
        role = last.get("role", "user")
        content = last.get("content", "")
        if role == "tool":
            try:
                data = json.loads(content)
            except (TypeError, json.JSONDecodeError):
                data = {}
            if isinstance(data, dict) and "result" in data:
                return {
                    "content": str(data["result"]),
                    "tool_calls": [],
                    "model": "mock-llm",
                    "usage": {"prompt_tokens": 4, "completion_tokens": 4, "total_tokens": 8},
                }
            return {
                "content": content,
                "tool_calls": [],
                "model": "mock-llm",
                "usage": {"prompt_tokens": 4, "completion_tokens": 4, "total_tokens": 8},
            }

        expr = _extract_expr(content)
        if expr:
            return {
                "content": "",
                "tool_calls": [{"name": "calculator", "arguments": {"expression": expr}}],
                "model": "mock-llm",
                "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
            }
        return {
            "content": f"Mock response to: {content[:100]}",
            "tool_calls": [],
            "model": "mock-llm",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        }

    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        return [[0.1] * 8 for _ in texts]


def _extract_expr(text: str) -> Optional[str]:
    if not text:
        return None
    compact = text.replace(" ", "")
    m = _EXPR.search(compact)
    if not m:
        return None
    expr = m.group(1)
    allowed = set("0123456789+-*/().%")
    if not all(c in allowed for c in expr):
        return None
    return expr
