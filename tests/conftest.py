"""Shared pytest fixtures. Engine is optional so type tests can run alone."""

import pytest


@pytest.fixture
def config():
    pytest.importorskip("yaml")
    from aetherflow.core.config import AetherConfig

    return AetherConfig(env="test", log_level="WARNING")


@pytest.fixture
def agent_config():
    pytest.importorskip("yaml")
    from aetherflow.core.config import AgentConfig

    return AgentConfig(name="test-agent", model="mock", temperature=0.0)
