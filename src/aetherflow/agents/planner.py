"""PlannerAgent — decomposes high-level goals into actionable plans."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.planner")


class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(role=AgentRole.PLANNER, **kwargs)

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        goal = context.get("goal") or context.get("input", "")
        logger.info(f"[{self.agent_id}] Planning for goal: {goal[:80]}...")
        plan = {
            "goal": goal,
            "steps": [
                {"id": 1, "action": "gather_information", "tools": ["web_search", "rag_query"]},
                {"id": 2, "action": "analyze_data", "depends_on": [1], "tools": ["python_repl"]},
                {"id": 3, "action": "synthesize_output", "depends_on": [2], "tools": ["report_generator"]},
                {"id": 4, "action": "review_quality", "depends_on": [3], "agent": "critic"},
            ],
            "estimated_iterations": 8,
            "risks": ["data_availability", "ambiguity_in_goal"],
        }
        return {"plan": plan, "confidence": 0.87}

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        plan = decision.get("plan", {})
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output=plan,
            metrics={"steps": len(plan.get("steps", [])), "confidence": decision.get("confidence", 0)},
        )
