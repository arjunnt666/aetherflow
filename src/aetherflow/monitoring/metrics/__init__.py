"""Lightweight in-process counters. Not Prometheus."""

from __future__ import annotations

from collections import defaultdict


class MetricsCollector:
    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)

    def inc(self, name: str, value: int = 1) -> None:
        self._counters[name] += value

    def get(self, name: str) -> int:
        return int(self._counters.get(name, 0))

    def snapshot(self) -> dict[str, int]:
        return dict(self._counters)


__all__ = ["MetricsCollector"]
