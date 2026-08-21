"""Deterministic agent tool loop: LLM proposes a call, registry runs it, LLM finishes."""

from __future__ import annotations

import json
from typing import Any

from aetherflow.integrations.llm.base import BaseLLMClient
from aetherflow.tools.registry import ToolRegistry


async def run_tool_loop(
    llm: BaseLLMClient,
    tools: ToolRegistry,
    goal: str,
    max_steps: int = 6,
) -> dict[str, Any]:
    messages: list[dict[str, str]] = [{"role": "user", "content": goal}]
    tool_trace: list[dict[str, Any]] = []
    for _ in range(max_steps):
        resp = await llm.complete(messages)
        calls = resp.get("tool_calls") or []
        if not calls:
            content = resp.get("content", "")
            return {
                "answer": _final_answer(content, tool_trace),
                "content": content,
                "tool_trace": tool_trace,
                "steps": len(tool_trace),
            }
        for call in calls:
            name = call["name"]
            args = call.get("arguments") or {}
            result = await tools.call(name, **args)
            tool_trace.append({"name": name, "arguments": args, "result": result})
            messages.append(
                {
                    "role": "tool",
                    "name": name,
                    "content": json.dumps(result),
                }
            )
    return {
        "answer": _final_answer("", tool_trace),
        "content": "",
        "tool_trace": tool_trace,
        "steps": len(tool_trace),
    }


def _final_answer(content: str, tool_trace: list[dict[str, Any]]) -> Any:
    for item in reversed(tool_trace):
        result = item.get("result") or {}
        if item.get("name") == "calculator" and "result" in result:
            return result["result"]
    text = (content or "").strip()
    if text:
        try:
            if "." in text:
                return float(text)
            return int(text)
        except ValueError:
            return text
    return content
