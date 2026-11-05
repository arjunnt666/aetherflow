"""Multi-source information gathering and synthesis."""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from aetherflow.agents.base import BaseAgent
from aetherflow.core.types import AgentRole, TaskResult, TaskStatus

logger = logging.getLogger("aetherflow.agents.researcher")


class ResearcherAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(role=AgentRole.RESEARCHER, **kwargs)

    async def think(self, context: dict[str, Any]) -> dict[str, Any]:
        query = context.get("query") or context.get("goal", "")
        logger.info(f"[{self.agent_id}] Researching: {query[:60]}...")
        return {
            "search_queries": [query],
        }

    async def act(self, decision: dict[str, Any]) -> TaskResult:
        findings = []
        if self.tools is not None and "web_search" in self.tools.list_tools():
            for q in decision["search_queries"][:1]:
                try:
                    res = await self.tools.call("web_search", query=q)
                    findings.extend({"source": "web", **r} for r in res.get("results", []))
                except Exception as e:  # offline, rate limited, etc.
                    logger.warning(f"web_search failed: {e}")
        notes = "\n".join(f"- {f['snippet']}" for f in findings) or "(no search results)"
        summary = await self.ask(
            f"Summarize what is known about: {decision['search_queries'][0]}\n\nNotes:\n{notes}"
        )
        return TaskResult(
            task_id=uuid4(),
            status=TaskStatus.COMPLETED,
            output={"summary": summary, "findings": findings, "citations": [f["url"] for f in findings if f.get("url")]},
        )
