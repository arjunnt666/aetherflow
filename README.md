# aetherflow

multi-agent layout with one tool loop that actually computes something.

agents, tools, pipelines. a lot of modules are still thin. the calculator path is not: MockLLM sees `2+2*3`, calls the calculator tool, and the answer is 8.

not a finished platform. a crate-style python package plus a working think/act/tool cycle you can pytest.

## works today

- pydantic types for messages, artifacts, statuses
- builtin calculator (`2+2*3` is 8, not 12)
- MockLLM + executor tool loop
- `aetherflow calc "2+2*3"`

## does not work yet

- production agent runs against live providers
- full pipeline execution without extra deps

## try it

```bash
pip install pydantic pydantic-settings pyyaml pytest pytest-asyncio
PYTHONPATH=src pytest tests/unit/core/test_types.py tests/unit/core/test_tool_loop.py tests/unit/tools/test_registry.py -q
PYTHONPATH=src python -m aetherflow.cli.main calc "2+2*3"
```

## license

apache-2.0
