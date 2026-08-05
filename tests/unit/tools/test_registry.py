import pytest
from aetherflow.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_load_builtins():
    reg = ToolRegistry()
    await reg.load_builtins()
    tools = reg.list_tools()
    assert "web_search" in tools
    assert "calculator" in tools


@pytest.mark.asyncio
async def test_calculator():
    reg = ToolRegistry()
    await reg.load_builtins()
    result = await reg.call("calculator", expression="2 + 2 * 3")
    assert result["result"] == 8
