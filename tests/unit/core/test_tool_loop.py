import pytest

from aetherflow.core.engine import AetherEngine
from aetherflow.core.tool_loop import run_tool_loop
from aetherflow.integrations.llm.mock import MockLLMClient
from aetherflow.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_tool_loop_calculator():
    reg = ToolRegistry()
    await reg.load_builtins()
    out = await run_tool_loop(MockLLMClient(), reg, "2+2*3")
    assert out["answer"] == 8
    assert out["steps"] >= 1
    assert out["tool_trace"][0]["name"] == "calculator"


@pytest.mark.asyncio
async def test_run_goal_uses_calculator():
    engine = AetherEngine.from_env()
    await engine.initialize()
    result = await engine.run_goal("compute 2+2*3")
    assert result.output["answer"] == 8
    assert result.metrics.get("tools_called", 0) >= 1
    await engine.shutdown()
