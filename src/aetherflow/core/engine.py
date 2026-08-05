"""
AetherEngine — the primary entry point for the AetherFlow platform.

Provides high-level APIs for creating agents, teams, pipelines, and
running autonomous workflows.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Optional, Sequence
from uuid import uuid4

from aetherflow.core.config import AetherConfig, AgentConfig
from aetherflow.core.orchestrator import Orchestrator
from aetherflow.core.runtime import AgentRuntime
from aetherflow.core.types import (
    AgentRole,
    Artifact,
    TeamTopology,
    TaskResult,
)
from aetherflow.agents.base import BaseAgent
from aetherflow.memory.fabric import MemoryFabric
from aetherflow.tools.registry import ToolRegistry
from aetherflow.monitoring.tracer import Tracer

logger = logging.getLogger("aetherflow.engine")


class AetherEngine:
    """
    Central engine for the AetherFlow multi-agent platform.

    Example:
        engine = AetherEngine.from_config("configs/dev.yaml")
        team = engine.create_team([...])
        result = await team.run("Analyze Q3 sales and produce a report")
    """

    def __init__(self, config: Optional[AetherConfig] = None):
        self.config = config or AetherConfig()
        self._runtime = AgentRuntime(self.config)
        self._orchestrator = Orchestrator(self.config, self._runtime)
        self._memory = MemoryFabric(self.config.memory)
        self._tools = ToolRegistry()
        self._tracer = Tracer(self.config.observability)
        self._teams: dict[str, Any] = {}
        self._initialized = False

        logger.info(
            "AetherEngine created",
            extra={"env": self.config.env, "version": "0.9.2"},
        )

    @classmethod
    def from_config(cls, path: str | Path) -> "AetherEngine":
        config = AetherConfig.from_yaml(path)
        return cls(config)

    @classmethod
    def from_env(cls) -> "AetherEngine":
        return cls(AetherConfig())

    async def initialize(self) -> None:
        if self._initialized:
            return
        logger.info("Initializing AetherFlow subsystems...")
        await self._memory.initialize()
        await self._tools.load_builtins()
        await self._tracer.start()
        self._initialized = True
        logger.info("AetherFlow ready")

    async def shutdown(self) -> None:
        logger.info("Shutting down AetherFlow...")
        await self._tracer.stop()
        await self._memory.close()
        self._initialized = False

    def create_agent(
        self,
        role: AgentRole | str = AgentRole.EXECUTOR,
        config: Optional[AgentConfig] = None,
        **kwargs: Any,
    ) -> BaseAgent:
        from aetherflow.agents.factory import AgentFactory
        cfg = config or AgentConfig(**kwargs)
        agent = AgentFactory.create(role, cfg, memory=self._memory, tools=self._tools)
        self._runtime.register(agent)
        return agent

    def create_team(
        self,
        agents: Sequence[BaseAgent],
        topology: TeamTopology | str = TeamTopology.HIERARCHICAL,
        name: Optional[str] = None,
    ) -> "AgentTeam":
        from aetherflow.agents.team import AgentTeam
        team_id = name or f"team-{uuid4().hex[:8]}"
        team = AgentTeam(
            team_id=team_id,
            agents=list(agents),
            topology=TeamTopology(topology),
            orchestrator=self._orchestrator,
            memory=self._memory,
        )
        self._teams[team_id] = team
        logger.info(f"Created team '{team_id}' with {len(agents)} agents ({topology})")
        return team

    async def run_pipeline(
        self,
        pipeline_path: str | Path,
        inputs: Optional[dict[str, Any]] = None,
    ) -> TaskResult:
        from aetherflow.pipelines.loader import PipelineLoader
        pipeline = PipelineLoader.load(pipeline_path)
        return await self._orchestrator.execute_pipeline(pipeline, inputs or {})

    async def run_goal(
        self,
        goal: str,
        agents: Optional[Sequence[BaseAgent]] = None,
        tools: Optional[list[str]] = None,
        max_iterations: int = 20,
    ) -> TaskResult:
        if not self._initialized:
            await self.initialize()
        if agents is None:
            agents = [
                self.create_agent(AgentRole.PLANNER),
                self.create_agent(AgentRole.EXECUTOR),
                self.create_agent(AgentRole.CRITIC),
            ]
        team = self.create_team(agents, topology=TeamTopology.HIERARCHICAL)
        return await team.run(goal=goal, tools=tools, max_iterations=max_iterations)

    @property
    def tools(self) -> ToolRegistry:
        return self._tools

    @property
    def memory(self) -> MemoryFabric:
        return self._memory

    def __repr__(self) -> str:
        return f"<AetherEngine env={self.config.env!r} agents={self._runtime.agent_count}>"
