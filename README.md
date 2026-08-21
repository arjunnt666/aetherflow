# aetherflow

multi-agent orchestration layout that can at least import its types.

agents, tools, pipelines, recovery notes. a lot of modules are still thin. the type tests run in CI without the full LLM stack.

not a finished platform. a crate-style python package map plus working Message / Artifact models.

## works today

- pydantic types for messages, artifacts, statuses
- `pytest tests/unit/core/test_types.py`

## does not work yet

- production agent runs against live providers
- full pipeline execution without extra deps

## try it

```bash
pip install pydantic pydantic-settings pyyaml pytest
PYTHONPATH=src pytest tests/unit/core/test_types.py -q
```

## license

apache-2.0
