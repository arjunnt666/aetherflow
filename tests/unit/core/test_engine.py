"""Unit tests for AetherEngine."""

import pytest
from aetherflow import AetherEngine, AgentConfig
from aetherflow.core.types import AgentRole


@pytest.mark.asyncio
async def test_engine_creation():
    engine = AetherEngine.from_env()
    assert engine is not None
    assert engine.config.env == "development"


@pytest.mark.asyncio
async def test_create_agent(engine):
    agent = engine.create_agent(AgentRole.EXECUTOR, AgentConfig(name="test"))
    assert agent.role == AgentRole.EXECUTOR
    assert agent.agent_id is not None


@pytest.mark.asyncio
async def test_create_team(engine):
    a1 = engine.create_agent(AgentRole.PLANNER)
    a2 = engine.create_agent(AgentRole.EXECUTOR)
    team = engine.create_team([a1, a2], topology="hierarchical")
    assert team is not None
    assert len(team.agents) == 2
