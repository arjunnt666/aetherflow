"""Shared pytest fixtures for AetherFlow tests."""

import pytest
from aetherflow.core.config import AetherConfig, AgentConfig
from aetherflow.core.engine import AetherEngine


@pytest.fixture
def config():
    return AetherConfig(env="test", log_level="WARNING")


@pytest.fixture
def agent_config():
    return AgentConfig(name="test-agent", model="mock", temperature=0.0)


@pytest.fixture
async def engine(config):
    eng = AetherEngine(config)
    await eng.initialize()
    yield eng
    await eng.shutdown()
