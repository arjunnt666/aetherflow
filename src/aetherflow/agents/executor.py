"""ExecutorAgent — performs concrete actions via tools and LLM calls."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.executor")


class ExecutorAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(role=AgentRole.EXECUTOR, **kwargs)

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        step = context.get("step") or context.get("input", {})
        logger.info(f"[{self.agent_id}] Preparing to execute: {step}")
        return {"action": "execute", "tool_calls": [], "reasoning": "Simulated tool selection."}

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output={"message": "Execution completed (simulated)", "decision": decision},
            metrics={"tokens_used": 0, "tools_called": 0},
        )
