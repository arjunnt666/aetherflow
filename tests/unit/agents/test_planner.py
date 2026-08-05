import pytest
from aetherflow.agents.planner import PlannerAgent
from aetherflow.core.config import AgentConfig
from aetherflow.core.types import TaskStatus


@pytest.mark.asyncio
async def test_planner_think_and_act():
    agent = PlannerAgent(config=AgentConfig(name="planner"))
    decision = await agent.think({"goal": "Write a report"})
    assert "plan" in decision
    result = await agent.act(decision)
    assert result.status == TaskStatus.COMPLETED
