"""Core type definitions for AetherFlow."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    PLANNER = "planner"
    EXECUTOR = "executor"
    CRITIC = "critic"
    RESEARCHER = "researcher"
    CODER = "coder"
    DATA_ANALYST = "data_analyst"
    COORDINATOR = "coordinator"
    MEMORY = "memory"
    GUARDIAN = "guardian"
    SPECIALIST = "specialist"
    CUSTOM = "custom"


class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class PipelineStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TeamTopology(str, Enum):
    HIERARCHICAL = "hierarchical"
    FLAT = "flat"
    SWARM = "swarm"
    PIPELINE = "pipeline"
    GRAPH = "graph"


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    AGENT = "agent"


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: MessageRole
    content: str
    agent_id: Optional[str] = None
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Artifact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    type: str
    content: Any
    mime_type: Optional[str] = None
    source_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskResult(BaseModel):
    task_id: UUID
    status: TaskStatus
    output: Any = None
    artifacts: list[Artifact] = Field(default_factory=list)
    error: Optional[str] = None
    metrics: dict[str, float] = Field(default_factory=dict)
    duration_ms: Optional[float] = None


class AgentState(BaseModel):
    agent_id: str
    role: AgentRole
    status: str = "idle"
    current_task: Optional[UUID] = None
    memory_tokens: int = 0
    tools_used: list[str] = Field(default_factory=list)
    last_active: datetime = Field(default_factory=datetime.utcnow)
