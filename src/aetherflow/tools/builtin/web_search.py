"""Simulated web search tool."""
from aetherflow.tools.base import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information on a given query."
    parameters = {"type": "object", "properties": {"query": {"type": "string"}, "num_results": {"type": "integer", "default": 5}}, "required": ["query"]}

    async def execute(self, query: str, num_results: int = 5, **kwargs) -> dict:
        return {"query": query, "results": [{"title": f"Result {i+1} for '{query}'", "url": f"https://example.com/result/{i+1}", "snippet": f"Simulated search result for: {query}"} for i in range(min(num_results, 3))]}
