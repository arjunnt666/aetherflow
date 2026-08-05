"""Working (short-term) memory — token-bounded context window."""

from __future__ import annotations
from typing import Any


class WorkingMemory:
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self._store: dict[str, Any] = {}
        self._order: list[str] = []

    def put(self, key: str, value: Any) -> None:
        if key not in self._store:
            self._order.append(key)
        self._store[key] = value
        while len(self._order) > 50:
            old = self._order.pop(0)
            self._store.pop(old, None)

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def search(self, query: str) -> list[dict[str, Any]]:
        q = query.lower()
        return [{"key": k, "value": v, "score": 1.0} for k, v in self._store.items() if q in str(v).lower() or q in k.lower()]

    def clear(self) -> None:
        self._store.clear()
        self._order.clear()

    def __len__(self) -> int:
        return len(self._store)
