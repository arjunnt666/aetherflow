# AetherFlow

multi-agent AI automation thing. kinda overbuilt on purpose.

you give it a goal, it spins up a little team of agents (planner, executor, critic, the usual suspects), they argue among themselves for a bit, and eventually something useful comes out. or at least something that *looks* useful.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)]()

---

## what it actually does

- **agents** that can plan, execute, critique, research, write code, etc.
- **teams** — hierarchical, flat, swarm, whatever mood you're in
- **memory** — short-term, episodic, semantic. the usual RAG-adjacent stuff
- **tools** — web search, calculator, time, echo (yes, echo). plug your own in
- **pipelines** — yaml-defined workflows with stages, deps, and quality gates
- **llm-agnostic** — openai, anthropic, or just the mock client if you don't feel like burning tokens today
- **observability** — traces + metrics so you can pretend you know what's going on
- **k8s / helm / docker** — because of course it has those

---

## quick start

```bash
git clone https://github.com/arjunnt666/aetherflow.git
cd aetherflow
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"
```

then the classic:

```python
from aetherflow import AetherEngine
from aetherflow.core.types import AgentRole

engine = AetherEngine.from_env()
await engine.initialize()

team = engine.create_team(
    agents=[
        engine.create_agent(AgentRole.PLANNER),
        engine.create_agent(AgentRole.EXECUTOR),
        engine.create_agent(AgentRole.CRITIC),
    ],
    topology="hierarchical",
)

result = await team.run("summarize why multi-agent systems are overhyped but also kinda cool")
print(result.output)
```

or just yell at the cli:

```bash
aetherflow run "make me a quarterly report that sounds expensive"
aetherflow list-tools
aetherflow doctor   # will tell you things are fine (they're not)
```

---

## layout (for the curious)

```
src/aetherflow/
  core/          # engine, orchestrator, runtime — the brain stem
  agents/        # planner, executor, critic, researcher, coder, etc.
  memory/        # working / episodic / semantic fabric
  tools/         # registry + builtins
  pipelines/     # yaml workflow runner
  integrations/  # llm clients (incl. the honest mock one)
  monitoring/    # traces + metrics
  cli/           # so you can feel productive in the terminal

configs/         # agent + pipeline yaml
deploy/          # k8s + helm (for when you want to deploy the hollow machine)
examples/        # copy-paste and go
tests/           # they exist
```

---

## honest notes

- a lot of the "AI" parts are stubbed / simulated right now. the architecture is real, the LLM calls are mostly cosplay until you drop in real keys.
- yes the folder count is high. no i don't regret it.
- if something breaks, it's probably the orchestrator. or the critic agent being too mean.

---

## license

apache 2.0 — do whatever, just don't sue me when the agents form a union.

---

built for fun. starred repos look better with stars ⭐
