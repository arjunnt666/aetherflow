"""
BaseAgent — abstract foundation for all AetherFlow agents.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import uuid4

from aetherflow.core.config import AgentConfig
from aetherflow.core.types import AgentRole, AgentState, Message, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents")


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the AetherFlow system.

    Subclasses must implement `think` and `act`.
    """

    def __init__(
        self,
        config: AgentConfig,
        role: AgentRole = AgentRole.CUSTOM,
        memory: Any = None,
        tools: Any = None,
        agent_id: Optional[str] = None,
    ):
        self.agent_id = agent_id or f"{role.value}-{uuid4().hex[:8]}"
        self.role = role
        self.config = config
        self.memory = memory
        self.tools = tools
        self._state = AgentState(agent_id=self.agent_id, role=role)
        self._history: list[Message] = []

        logger.debug(f"Agent created: {self.agent_id} ({role.value})")

    @property
    def state(self) -> AgentState:
        return self._state

    @abstractmethod
    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        """Reason about the current context and produce a plan or decision."""
        ...

    @abstractmethod
    async def act(self, decision: dict[str, Any]) -> TaskResult:
        """Execute the decision (tool calls, generation, etc.)."""
        ...

    async def run(self, task: dict[str, Any]) -> TaskResult:
        """Full think → act cycle for a single task."""
        self._state.status = "running"
        self._state.current_task = task.get("id")

        try:
            decision = await self.think(task)
            result = await self.act(decision)
            self._state.status = "idle"
            return result
        except Exception as e:
            logger.exception(f"Agent {self.agent_id} failed")
            self._state.status = "error"
            return TaskResult(
                task_id=task.get("id", uuid4()),
                status=TaskStatus.FAILED,
                error=str(e),
            )

    def add_message(self, message: Message) -> None:
        self._history.append(message)
        window = self.config.memory_window
        if len(self._history) > window:
            self._history = self._history[-window:]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id!r} role={self.role.value}>"
