"""Pipeline execution engine (stage runner)."""

from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger("aetherflow.pipelines")


class PipelineEngine:
    def __init__(self, orchestrator: Any = None):
        self.orchestrator = orchestrator

    async def run(self, pipeline: Any, inputs: dict[str, Any] | None = None) -> dict:
        logger.info(f"PipelineEngine running: {pipeline.name}")
        if self.orchestrator:
            result = await self.orchestrator.execute_pipeline(pipeline, inputs or {})
            return result.model_dump() if hasattr(result, "model_dump") else result
        return {"status": "simulated", "pipeline": pipeline.name}
