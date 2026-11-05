"""
Coordinates multi-agent execution, task routing,
and pipeline stage management.
"""

from __future__ import annotations

import asyncio
import time
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
            started = time.perf_counter()
            stages = getattr(pipeline, "stages", [])
            context: dict[str, Any] = {"inputs": inputs, "artifacts": []}
            for i, stage in enumerate(stages):
                stage_name = stage.get("name", f"stage-{i}")
                logger.info(f"Executing stage: {stage_name}")
                agent = self._agent_for(stage)
                if agent is None:
                    raise RuntimeError(f"no agent registered for stage {stage_name!r} (role {stage.get('agent')!r})")
                prior = {a["stage"]: a["output"] for a in context["artifacts"]}
                task = {
                    "goal": stage.get("prompt") or stage_name,
                    "inputs": inputs,
                    "depends": {d: prior.get(d) for d in stage.get("depends_on", [])},
                }
                result = await agent.run(task)
                if result.status == TaskStatus.FAILED:
                    raise RuntimeError(f"stage {stage_name} failed: {result.error}")
                context["artifacts"].append({"stage": stage_name, "status": "completed", "output": result.output})
                self._active_pipelines[pipeline_id]["stages_completed"] = i + 1
            self._active_pipelines[pipeline_id]["status"] = PipelineStatus.COMPLETED
            return TaskResult(
                task_id=uuid4(),
                status=TaskStatus.COMPLETED,
                output=context,
                metrics={"stages": float(len(stages)), "duration_ms": (time.perf_counter() - started) * 1000},
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
        return await agent.run(task)

    def _agent_for(self, stage: dict[str, Any]) -> Any:
        """Stage `agent` can be an agent id or a role; first match by role wins."""
        want = stage.get("agent")
        agent = self.runtime.get_agent(want) if want else None
        if agent is not None:
            return agent
        for a in self.runtime.list_agents():
            if a.role.value == want:
                return a
        return None

    def get_pipeline_status(self, pipeline_id: str) -> Optional[dict]:
        return self._active_pipelines.get(pipeline_id)
