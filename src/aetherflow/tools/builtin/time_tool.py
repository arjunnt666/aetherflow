from datetime import datetime, timezone
from aetherflow.tools.base import BaseTool


class CurrentTimeTool(BaseTool):
    name = "current_time"
    description = "Get the current UTC time."
    parameters = {"type": "object", "properties": {}}

    async def execute(self, **kwargs) -> dict:
        now = datetime.now(timezone.utc)
        return {"utc": now.isoformat(), "unix": int(now.timestamp()), "human": now.strftime("%Y-%m-%d %H:%M:%S UTC")}
