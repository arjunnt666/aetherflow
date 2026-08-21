"""AetherFlow — multi-agent orchestration layout."""

from aetherflow.core.types import (
    AgentRole,
    Artifact,
    Message,
    PipelineStatus,
    TaskStatus,
    TeamTopology,
)

__version__ = "0.9.2"
__all__ = [
    "AetherEngine",
    "AetherConfig",
    "AgentConfig",
    "AgentRole",
    "TaskStatus",
    "PipelineStatus",
    "Message",
    "Artifact",
    "TeamTopology",
]


def __getattr__(name: str):
    if name == "AetherEngine":
        from aetherflow.core.engine import AetherEngine

        return AetherEngine
    if name == "AetherConfig":
        from aetherflow.core.config import AetherConfig

        return AetherConfig
    if name == "AgentConfig":
        from aetherflow.core.config import AgentConfig

        return AgentConfig
    raise AttributeError(name)
