"""Minimal example: create a team and run a simple goal."""

import asyncio
from aetherflow import AetherEngine, AgentConfig
from aetherflow.core.types import AgentRole


async def main():
    engine = AetherEngine.from_env()
    await engine.initialize()

    planner = engine.create_agent(AgentRole.PLANNER, AgentConfig(name="planner"))
    executor = engine.create_agent(AgentRole.EXECUTOR, AgentConfig(name="executor"))
    critic = engine.create_agent(AgentRole.CRITIC, AgentConfig(name="critic"))

    team = engine.create_team([planner, executor, critic], topology="hierarchical", name="demo-team")
    result = await team.run(goal="Explain the benefits of multi-agent systems", max_iterations=5)

    print("\n=== RESULT ===")
    print(result.output.get("summary", result.output))
    await engine.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
