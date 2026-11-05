"""Software engineering specialist."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.coder")


class CoderAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(role=AgentRole.CODER, **kwargs)

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        task = context.get("task") or context.get("goal", "")
        logger.info(f"[{self.agent_id}] Coding task: {str(task)[:60]}...")
        return {
            "approach": "implement_with_tests",
            "language": "python",
            "files_to_touch": [],
            "task": str(task),
        }

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        task = decision.get("task", "")
        code = await self.ask(
            f"Write {decision['language']} code for the task below, followed by pytest tests.\n\n{task}"
        )
        return TaskResult(task_id=uuid4(), status=TaskStatus.COMPLETED, output={"code": code})
