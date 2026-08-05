"""Episodic memory — stores interaction histories and events over time."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4


class EpisodicMemory:
    def __init__(self, retention_days: int = 30):
        self.retention_days = retention_days
        self._events: list[dict[str, Any]] = []

    async def append(self, key: str, value: Any) -> str:
        event_id = str(uuid4())
        self._events.append({"id": event_id, "key": key, "value": value, "timestamp": datetime.utcnow().isoformat()})
        await self._prune()
        return event_id

    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        q = query.lower()
        matches = [e for e in reversed(self._events) if q in str(e.get("value", "")).lower() or q in e.get("key", "").lower()]
        return matches[:limit]

    async def _prune(self) -> None:
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        self._events = [e for e in self._events if datetime.fromisoformat(e["timestamp"]) > cutoff]
