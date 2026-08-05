"""Prometheus-compatible metrics collector (in-memory)."""

from __future__ import annotations
from collections import defaultdict
from typing import Optional


class MetricsCollector:
    def __init__(self):
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def inc(self, name: str, value: float = 1.0, labels: Optional[dict] = None) -> None:
        key = self._key(name, labels)
        self._counters[key] += value

    def set_gauge(self, name: str, value: float, labels: Optional[dict] = None) -> None:
        key = self._key(name, labels)
        self._gauges[key] = value

    def observe(self, name: str, value: float, labels: Optional[dict] = None) -> None:
        key = self._key(name, labels)
        self._histograms[key].append(value)

    def _key(self, name: str, labels: Optional[dict]) -> str:
        if not labels:
            return name
        label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def export(self) -> dict:
        return {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": {k: {"count": len(v), "sum": sum(v)} for k, v in self._histograms.items()},
        }
