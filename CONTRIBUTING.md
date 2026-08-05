# Contributing to AetherFlow

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/arjunnt666/aetherflow.git
cd aetherflow
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Guidelines

1. Code style: We use ruff and mypy.
2. Tests: Add unit tests for new features.
3. Docs: Update relevant markdown under docs/.
4. Agents: New specialized agents live under src/aetherflow/agents/specialized/.
5. Commit messages: Prefer conventional commits (feat:, fix:, docs:).

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes + tests
4. Ensure CI passes
5. Open a PR with a clear description
