from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseLLMClient(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict[str, str]], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2048, **kwargs: Any) -> dict[str, Any]:
        ...

    @abstractmethod
    async def embed(self, texts: list[str], model: Optional[str] = None) -> list[list[float]]:
        ...
