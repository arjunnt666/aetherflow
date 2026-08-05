"""Load pipeline definitions from YAML."""

from __future__ import annotations
from pathlib import Path
from typing import Any
from uuid import uuid4
import yaml


class Pipeline:
    def __init__(self, data: dict[str, Any]):
        self.id = data.get("id", str(uuid4()))
        self.name = data.get("name", "unnamed")
        self.version = data.get("version", "1.0.0")
        self.triggers = data.get("triggers", [])
        self.stages = data.get("stages", [])
        self.metadata = data.get("metadata", {})

    def __repr__(self) -> str:
        return f"<Pipeline {self.name!r} v{self.version} stages={len(self.stages)}>"


class PipelineLoader:
    @staticmethod
    def load(path: str | Path) -> Pipeline:
        path = Path(path)
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return Pipeline(data)

    @staticmethod
    def load_from_dict(data: dict[str, Any]) -> Pipeline:
        return Pipeline(data)
