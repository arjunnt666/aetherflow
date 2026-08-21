"""ExecutorAgent — performs concrete actions via tools and LLM calls."""

from __future__ import annotations

import logging
from typing import Any, Optional
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus
from aetherflow.integrations.llm.base import BaseLLMClient

logger = logging.getLogger("aetherflow.agents.executor")


class ExecutorAgent(BaseAgent):
    def __init__(self, llm: Optional[BaseLLMClient] = None, **kwargs):
        super().__init__(role=AgentRole.EXECUTOR, **kwargs)
        self.llm = llm

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        goal = context.get("goal") or context.get("input") or context.get("step") or ""
        if isinstance(goal, dict):
            goal = str(goal)
        logger.info(f"[{self.agent_id}] Preparing to execute: {goal}")
        return {"action": "execute", "goal": str(goal)}

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        goal = str(decision.get("goal") or "")
        if self.llm is not None and self.tools is not None:
            from aetherflow.core.tool_loop import run_tool_loop

            out = await run_tool_loop(self.llm, self.tools, goal)
            return TaskResult(
                task_id=uuid4(),
                status=TaskStatus.COMPLETED,
                output=out,
                metrics={"tokens_used": 0.0, "tools_called": float(out.get("steps", 0))},
            )
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output={"message": "Execution completed (simulated)", "decision": decision},
            metrics={"tokens_used": 0, "tools_called": 0},
        )
