.PHONY: install test lint typecheck clean docker docs

install:
	pip install -e ".[all]"

test:
	pytest tests/ -v --cov=aetherflow --cov-report=term-missing

lint:
	ruff check src/ tests/

typecheck:
	mypy src/aetherflow --ignore-missing-imports

clean:
	rm -rf build/ dist/ *.egg-info .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker:
	docker build -t aetherflow:0.9.2 .

docs:
	@echo "Docs are in docs/"
