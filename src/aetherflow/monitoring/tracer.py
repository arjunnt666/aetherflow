"""OpenTelemetry-style tracer (simplified)."""

from __future__ import annotations
import logging
from typing import Any, Optional
from aetherflow.core.config import ObservabilityConfig

logger = logging.getLogger("aetherflow.tracer")


class Tracer:
    def __init__(self, config: ObservabilityConfig):
        self.config = config
        self._spans: list[dict] = []
        self._active = False

    async def start(self) -> None:
        if self.config.enable_tracing:
            self._active = True
            logger.info("Tracer started")

    async def stop(self) -> None:
        self._active = False

    def start_span(self, name: str, attributes: Optional[dict] = None) -> "Span":
        return Span(name, attributes or {}, self)

    def record(self, span: dict) -> None:
        if self._active:
            self._spans.append(span)


class Span:
    def __init__(self, name: str, attributes: dict, tracer: Tracer):
        self.name = name
        self.attributes = attributes
        self.tracer = tracer

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.tracer.record({"name": self.name, "attributes": self.attributes})

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        self.tracer.record({"name": self.name, "attributes": self.attributes})
