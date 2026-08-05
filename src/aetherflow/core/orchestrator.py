"""
Orchestrator — coordinates multi-agent execution, task routing,
and pipeline stage management.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional
from uuid import uuid4

from aetherflow.core.config import AetherConfig
from aetherflow.core.runtime import AgentRuntime
from aetherflow.core.types import TaskResult, TaskStatus, PipelineStatus

logger = logging.getLogger("aetherflow.orchestrator")


class Orchestrator:
    def __init__(self, config: AetherConfig, runtime: AgentRuntime):
        self.config = config
        self.runtime = runtime
        self._active_pipelines: dict[str, Any] = {}
        self._task_queue: asyncio.Queue = asyncio.Queue()

    async def execute_pipeline(self, pipeline: Any, inputs: dict[str, Any]) -> TaskResult:
        pipeline_id = getattr(pipeline, "id", str(uuid4()))
        logger.info(f"Starting pipeline {pipeline_id}", extra={"name": getattr(pipeline, "name", None)})
        self._active_pipelines[pipeline_id] = {"status": PipelineStatus.RUNNING, "stages_completed": 0}
        try:
            stages = getattr(pipeline, "stages", [])
            context: dict[str, Any] = {"inputs": inputs, "artifacts": []}
            for i, stage in enumerate(stages):
                stage_name = stage.get("name", f"stage-{i}")
                logger.info(f"Executing stage: {stage_name}")
                await asyncio.sleep(0.05)
                context["artifacts"].append({"stage": stage_name, "status": "completed", "output": f"[simulated output for {stage_name}]"})
                self._active_pipelines[pipeline_id]["stages_completed"] = i + 1
            self._active_pipelines[pipeline_id]["status"] = PipelineStatus.COMPLETED
            return TaskResult(
                task_id=uuid4(),
                status=TaskStatus.COMPLETED,
                output=context,
                metrics={"stages": len(stages), "duration_ms": 50.0 * len(stages)},
            )
        except Exception as e:
            logger.exception(f"Pipeline {pipeline_id} failed")
            self._active_pipelines[pipeline_id]["status"] = PipelineStatus.FAILED
            return TaskResult(task_id=uuid4(), status=TaskStatus.FAILED, error=str(e))

    async def dispatch_task(self, agent_id: str, task: dict[str, Any]) -> TaskResult:
        agent = self.runtime.get_agent(agent_id)
        if agent is None:
            return TaskResult(task_id=uuid4(), status=TaskStatus.FAILED, error=f"Agent {agent_id} not found")
        logger.debug(f"Dispatching task to {agent_id}")
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output={"message": f"Task processed by {agent_id}", "echo": task},
        )

    def get_pipeline_status(self, pipeline_id: str) -> Optional[dict]:
        return self._active_pipelines.get(pipeline_id)
