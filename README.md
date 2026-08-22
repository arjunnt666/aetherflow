Aetherflow status

The GitHub description still says enterprise grade. ignore that. I have not shipped a platform.

What I can show with pytest: pydantic types for messages, artifacts, statuses. a builtin calculator. MockLLM sees `2+2*3`, calls the calculator tool, and the answer is 8 (not 12). that think / act / tool cycle is the part that is real. a lot of other modules are still thin.

Install the bits the tests actually import, then:

```
pip install pydantic pydantic-settings pyyaml pytest pytest-asyncio
PYTHONPATH=src pytest tests/unit/core/test_types.py tests/unit/core/test_tool_loop.py tests/unit/tools/test_registry.py -q
PYTHONPATH=src python -m aetherflow.cli.main calc "2+2*3"
```

live providers are not wired. full pipeline execution wants extra deps I have not made required.

Apache-2.0
