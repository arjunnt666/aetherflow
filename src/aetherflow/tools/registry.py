"""ToolRegistry — discovers, registers, and invokes tools."""

from __future__ import annotations
import logging
from typing import Any, Optional

logger = logging.getLogger("aetherflow.tools")


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Any] = {}

    def register(self, name: str, tool: Any, overwrite: bool = False) -> None:
        if name in self._tools and not overwrite:
            raise ValueError(f"Tool '{name}' already registered")
        self._tools[name] = tool
        logger.debug(f"Registered tool: {name}")

    def get(self, name: str) -> Optional[Any]:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    async def call(self, name: str, **kwargs: Any) -> Any:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Tool '{name}' not found")
        if hasattr(tool, "execute"):
            return await tool.execute(**kwargs)
        if callable(tool):
            result = tool(**kwargs)
            if hasattr(result, "__await__"):
                return await result
            return result
        raise TypeError(f"Tool '{name}' is not callable")

    async def load_builtins(self) -> None:
        from aetherflow.tools.builtin import web_search, calculator, current_time, echo
        for t in [web_search, calculator, current_time, echo]:
            self.register(t.name, t)
        logger.info(f"Loaded {len(self._tools)} built-in tools")
