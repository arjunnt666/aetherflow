"""
AetherFlow — Enterprise Multi-Agent AI Automation Platform

A production-grade framework for building, orchestrating, and scaling
autonomous multi-agent systems and intelligent workflows.
"""

from aetherflow.core.engine import AetherEngine
from aetherflow.core.config import AetherConfig, AgentConfig
from aetherflow.core.types import (
    AgentRole,
    TaskStatus,
    PipelineStatus,
    Message,
    Artifact,
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
