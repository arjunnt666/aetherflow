"""Web search via DuckDuckGo's instant answer API (no key needed).

It only returns abstracts and related topics, not a full result page, but
it's real data and good enough for an agent to ground a short answer.
"""

import httpx

from aetherflow.tools.base import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information on a given query."
    parameters = {
        "type": "object",
        "properties": {"query": {"type": "string"}, "num_results": {"type": "integer", "default": 5}},
        "required": ["query"],
    }

    async def execute(self, query: str, num_results: int = 5, **kwargs) -> dict:
        async with httpx.AsyncClient(timeout=10) as http:
            r = await http.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            )
            r.raise_for_status()
            data = r.json()

        results = []
        if data.get("AbstractText"):
            results.append(
                {"title": data.get("Heading", query), "url": data.get("AbstractURL", ""), "snippet": data["AbstractText"]}
            )
        for t in data.get("RelatedTopics", []):
            for item in t.get("Topics", [t]):
                if item.get("Text"):
                    results.append({"title": item["Text"].split(" - ")[0], "url": item.get("FirstURL", ""), "snippet": item["Text"]})
        return {"query": query, "results": results[:num_results]}
