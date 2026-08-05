"""Configuration management for AetherFlow."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class LLMConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4o"
    temperature: float = 0.2
    max_tokens: int = 4096
    top_p: float = 1.0
    timeout: float = 120.0
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    extra: dict[str, Any] = Field(default_factory=dict)


class AgentConfig(BaseModel):
    name: Optional[str] = None
    role: str = "executor"
    model: str = "gpt-4o"
    temperature: float = 0.3
    max_iterations: int = 15
    tools: list[str] = Field(default_factory=list)
    system_prompt: Optional[str] = None
    memory_enabled: bool = True
    memory_window: int = 20
    timeout_seconds: float = 300.0
    retry_attempts: int = 3
    llm: Optional[LLMConfig] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryConfig(BaseModel):
    backend: str = "hybrid"
    vector_store: str = "qdrant"
    embedding_model: str = "text-embedding-3-small"
    max_working_tokens: int = 8000
    episodic_retention_days: int = 30
    semantic_top_k: int = 8
    enable_graph: bool = True


class SecurityConfig(BaseModel):
    enable_rbac: bool = True
    enable_sandbox: bool = True
    enable_pii_redaction: bool = True
    audit_log: bool = True
    allowed_tools: list[str] = Field(default_factory=list)
    blocked_domains: list[str] = Field(default_factory=list)


class ObservabilityConfig(BaseModel):
    enable_tracing: bool = True
    enable_metrics: bool = True
    log_level: str = "INFO"
    otel_endpoint: Optional[str] = None
    prometheus_port: int = 9090


class AetherConfig(BaseSettings):
    env: str = "development"
    log_level: str = "INFO"
    data_dir: Path = Path("./data")
    config_dir: Path = Path("./configs")

    llm: LLMConfig = Field(default_factory=LLMConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)

    max_concurrent_agents: int = 32
    default_timeout: float = 600.0
    enable_self_healing: bool = True

    class Config:
        env_prefix = "AETHERFLOW_"
        env_nested_delimiter = "__"

    @classmethod
    def from_yaml(cls, path: str | Path) -> "AetherConfig":
        path = Path(path)
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)

    def to_yaml(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(self.model_dump(mode="json"), f, default_flow_style=False)
