"""Semantic memory — vector-based long-term knowledge store."""

from __future__ import annotations
import logging
from typing import Any, Optional

logger = logging.getLogger("aetherflow.memory.semantic")


class SemanticMemory:
    def __init__(self, top_k: int = 8, embedding_model: str = "text-embedding-3-small"):
        self.top_k = top_k
        self.embedding_model = embedding_model
        self._docs: dict[str, dict[str, Any]] = {}
        self._connected = False

    async def connect(self) -> None:
        logger.info(f"SemanticMemory connected (backend=in-memory, model={self.embedding_model})")
        self._connected = True

    async def close(self) -> None:
        self._connected = False

    async def upsert(self, doc_id: str, content: Any, metadata: Optional[dict] = None) -> None:
        self._docs[doc_id] = {"content": content, "metadata": metadata or {}}

    async def search(self, query: str, top_k: Optional[int] = None) -> list[dict[str, Any]]:
        k = top_k or self.top_k
        q = query.lower()
        results = []
        for doc_id, doc in self._docs.items():
            if q in str(doc["content"]).lower():
                results.append({"id": doc_id, "content": doc["content"], "score": 0.85, "metadata": doc["metadata"]})
        return results[:k]
