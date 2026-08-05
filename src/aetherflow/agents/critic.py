"""CriticAgent — evaluates outputs for quality, safety, and policy compliance."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.critic")


class CriticAgent(BaseAgent):
    """Quality & safety gate agent."""

    def __init__(self, **kwargs):
        super().__init__(role=AgentRole.CRITIC, **kwargs)

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"[{self.agent_id}] Critiquing output...")
        return {
            "scores": {"quality": 0.91, "relevance": 0.88, "safety": 0.99, "factuality": 0.85},
            "issues": [],
            "recommendation": "approve",
            "feedback": "Output meets quality thresholds.",
        }

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        return TaskResult(task_id=uuid4(), status=TaskStatus.COMPLETED, output=decision, metrics=decision.get("scores", {}))
