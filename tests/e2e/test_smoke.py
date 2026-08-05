"""End-to-end smoke tests."""

import pytest
from aetherflow import AetherEngine


@pytest.mark.asyncio
async def test_full_goal_run():
    engine = AetherEngine.from_env()
    await engine.initialize()
    result = await engine.run_goal("Summarize the concept of multi-agent systems")
    assert result is not None
    assert result.status.value in ("completed", "failed")
    await engine.shutdown()
