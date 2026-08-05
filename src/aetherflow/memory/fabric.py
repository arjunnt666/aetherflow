"""
MemoryFabric — unified interface over working, episodic, and semantic memory.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from aetherflow.core.config import MemoryConfig
from aetherflow.memory.working import WorkingMemory
from aetherflow.memory.episodic import EpisodicMemory
from aetherflow.memory.semantic import SemanticMemory

logger = logging.getLogger("aetherflow.memory")


class MemoryFabric:
    def __init__(self, config: MemoryConfig):
        self.config = config
        self.working = WorkingMemory(max_tokens=config.max_working_tokens)
        self.episodic = EpisodicMemory(retention_days=config.episodic_retention_days)
        self.semantic = SemanticMemory(top_k=config.semantic_top_k, embedding_model=config.embedding_model)
        self._initialized = False

    async def initialize(self) -> None:
        logger.info("Initializing MemoryFabric...")
        await self.semantic.connect()
        self._initialized = True

    async def close(self) -> None:
        await self.semantic.close()
        self._initialized = False

    async def store(self, key: str, value: Any, memory_type: str = "working") -> None:
        if memory_type == "working":
            self.working.put(key, value)
        elif memory_type == "episodic":
            await self.episodic.append(key, value)
        elif memory_type == "semantic":
            await self.semantic.upsert(key, value)
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")

    async def retrieve(self, query: str, memory_types: Optional[list[str]] = None, top_k: int = 5) -> list[dict[str, Any]]:
        memory_types = memory_types or ["working", "episodic", "semantic"]
        results = []
        if "working" in memory_types:
            results.extend(self.working.search(query))
        if "episodic" in memory_types:
            results.extend(await self.episodic.search(query, limit=top_k))
        if "semantic" in memory_types:
            results.extend(await self.semantic.search(query, top_k=top_k))
        return results[:top_k]

    def clear_working(self) -> None:
        self.working.clear()
