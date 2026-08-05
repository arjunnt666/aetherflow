"""Safe calculator tool."""
from aetherflow.tools.base import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate a mathematical expression."
    parameters = {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}

    async def execute(self, expression: str, **kwargs) -> dict:
        try:
            allowed = set("0123456789+-*/().% ")
            if not all(c in allowed for c in expression):
                return {"error": "Invalid characters in expression"}
            result = eval(expression, {"__builtins__": {}}, {})
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"expression": expression, "error": str(e)}
