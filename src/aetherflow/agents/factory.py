"""AgentFactory — creates specialized agents from role + config."""

from __future__ import annotations

from typing import Any

from aetherflow.core.config import AgentConfig
from aetherflow.core.types import AgentRole
from aetherflow.agents.base import BaseAgent


class AgentFactory:
    _registry: dict[AgentRole, type] = {}

    @classmethod
    def register(cls, role: AgentRole, agent_cls: type) -> None:
        cls._registry[role] = agent_cls

    @classmethod
    def create(cls, role: AgentRole | str, config: AgentConfig, memory: Any = None, tools: Any = None) -> BaseAgent:
        if isinstance(role, str):
            role = AgentRole(role)
        if role not in cls._registry:
            cls._populate_registry()
        agent_cls = cls._registry.get(role)
        if agent_cls is None:
            from aetherflow.agents.executor import ExecutorAgent
            agent_cls = ExecutorAgent
        return agent_cls(config=config, memory=memory, tools=tools)

    @classmethod
    def _populate_registry(cls) -> None:
        from aetherflow.agents.planner import PlannerAgent
        from aetherflow.agents.executor import ExecutorAgent
        from aetherflow.agents.critic import CriticAgent
        from aetherflow.agents.researcher import ResearcherAgent
        from aetherflow.agents.coder import CoderAgent
        from aetherflow.agents.coordinator import CoordinatorAgent
        cls._registry = {
            AgentRole.PLANNER: PlannerAgent,
            AgentRole.EXECUTOR: ExecutorAgent,
            AgentRole.CRITIC: CriticAgent,
            AgentRole.RESEARCHER: ResearcherAgent,
            AgentRole.CODER: CoderAgent,
            AgentRole.COORDINATOR: CoordinatorAgent,
            AgentRole.DATA_ANALYST: ExecutorAgent,
            AgentRole.MEMORY: ExecutorAgent,
            AgentRole.GUARDIAN: CriticAgent,
            AgentRole.SPECIALIST: ExecutorAgent,
            AgentRole.CUSTOM: ExecutorAgent,
        }
