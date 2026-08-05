"""AgentTeam — coordinates a group of agents under a chosen topology."""

from __future__ import annotations

import logging
from typing import Any, Optional, Sequence
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import TeamTopology, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.team")


class AgentTeam:
    def __init__(
        self,
        team_id: str,
        agents: Sequence[BaseAgent],
        topology: TeamTopology = TeamTopology.HIERARCHICAL,
        orchestrator: Any = None,
        memory: Any = None,
    ):
        self.team_id = team_id
        self.agents = list(agents)
        self.topology = topology
        self.orchestrator = orchestrator
        self.memory = memory

    async def run(
        self,
        goal: str,
        tools: Optional[list[str]] = None,
        max_iterations: int = 20,
        **kwargs: Any,
    ) -> TaskResult:
        logger.info(
            f"Team {self.team_id} starting run",
            extra={"goal": goal[:80], "agents": len(self.agents), "topology": self.topology.value},
        )
        results = []
        for i, agent in enumerate(self.agents):
            logger.info(f"  → Invoking {agent.agent_id}")
            result = await agent.run({"goal": goal, "iteration": i, "tools": tools or []})
            results.append(result)

        summary = (
            f"Team '{self.team_id}' completed goal after {len(self.agents)} agent turns. "
            f"Topology: {self.topology.value}. "
            f"(Simulated run — integrate real LLM backends for production use.)"
        )
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output={
                "summary": summary,
                "goal": goal,
                "agent_results": [r.model_dump() for r in results],
                "iterations": len(self.agents),
            },
            metrics={"agents_invoked": len(self.agents), "topology": self.topology.value},
        )

    def __repr__(self) -> str:
        return f"<AgentTeam id={self.team_id!r} agents={len(self.agents)} topology={self.topology.value}>"
