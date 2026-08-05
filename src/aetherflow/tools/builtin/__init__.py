from aetherflow.tools.builtin.web_search import WebSearchTool
from aetherflow.tools.builtin.calculator import CalculatorTool
from aetherflow.tools.builtin.time_tool import CurrentTimeTool
from aetherflow.tools.builtin.echo import EchoTool

web_search = WebSearchTool()
calculator = CalculatorTool()
current_time = CurrentTimeTool()
echo = EchoTool()

__all__ = ["web_search", "calculator", "current_time", "echo"]
