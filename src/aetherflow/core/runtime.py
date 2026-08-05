"""
AgentRuntime — manages the lifecycle and resource allocation of agents.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from aetherflow.core.config import AetherConfig
from aetherflow.agents.base import BaseAgent

logger = logging.getLogger("aetherflow.runtime")


class AgentRuntime:
    def __init__(self, config: AetherConfig):
        self.config = config
        self._agents: dict[str, BaseAgent] = {}
        self._max_agents = config.max_concurrent_agents

    def register(self, agent: BaseAgent) -> None:
        if len(self._agents) >= self._max_agents:
            raise RuntimeError(f"Maximum concurrent agents ({self._max_agents}) reached")
        self._agents[agent.agent_id] = agent
        logger.debug(f"Registered agent {agent.agent_id} ({agent.role})")

    def unregister(self, agent_id: str) -> None:
        self._agents.pop(agent_id, None)

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self._agents.get(agent_id)

    def list_agents(self) -> list[BaseAgent]:
        return list(self._agents.values())

    @property
    def agent_count(self) -> int:
        return len(self._agents)

    def health(self) -> dict[str, Any]:
        return {
            "agents_registered": self.agent_count,
            "max_agents": self._max_agents,
            "status": "healthy",
        }
