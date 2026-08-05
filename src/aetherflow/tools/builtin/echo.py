from aetherflow.tools.base import BaseTool


class EchoTool(BaseTool):
    name = "echo"
    description = "Echo back the provided message (useful for testing)."
    parameters = {"type": "object", "properties": {"message": {"type": "string"}}, "required": ["message"]}

    async def execute(self, message: str, **kwargs) -> dict:
        return {"echo": message}
