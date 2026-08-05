"""Base tool abstractions and decorator."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from functools import wraps


class BaseTool(ABC):
    name: str = "base_tool"
    description: str = ""
    parameters: dict = {}

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        ...

    def to_openai_schema(self) -> dict:
        return {"type": "function", "function": {"name": self.name, "description": self.description, "parameters": self.parameters}}


def tool(name: str, description: str = "", parameters: Optional[dict] = None):
    def decorator(fn: Callable):
        @wraps(fn)
        async def wrapper(**kwargs):
            return await fn(**kwargs) if asyncio_iscoroutine(fn) else fn(**kwargs)
        wrapper._tool_name = name
        wrapper._tool_description = description
        wrapper._tool_parameters = parameters or {}
        return wrapper
    return decorator


def asyncio_iscoroutine(fn):
    import asyncio
    return asyncio.iscoroutinefunction(fn)
