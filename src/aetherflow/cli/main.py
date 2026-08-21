"""
AetherFlow CLI — entry point for the `aetherflow` command.
"""

from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="aetherflow",
    help="AetherFlow — Enterprise Multi-Agent AI Automation Platform",
    add_completion=False,
)
console = Console()


@app.command()
def version():
    from aetherflow import __version__
    console.print(f"[bold cyan]AetherFlow[/] v{__version__}")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Bind host"),
    port: int = typer.Option(8080, help="Bind port"),
    config: Optional[str] = typer.Option(None, help="Path to config YAML"),
):
    console.print(f"[green]Starting AetherFlow server on {host}:{port}[/]")
    console.print("[dim](Server implementation is a stub in this release)[/]")
    if config:
        console.print(f"Config: {config}")


@app.command()
def run(
    goal: str = typer.Argument(..., help="Natural language goal to execute"),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    max_iterations: int = typer.Option(10, "--max-iter"),
):
    console.print(f"[bold]Goal:[/] {goal}")
    console.print("[dim]Initializing engine...[/]")

    async def _run():
        from aetherflow import AetherEngine
        engine = AetherEngine.from_config(config) if config else AetherEngine.from_env()
        await engine.initialize()
        result = await engine.run_goal(goal, max_iterations=max_iterations)
        console.print("\n[bold green]Result:[/]")
        console.print(result.output.get("summary", result.output) if isinstance(result.output, dict) else result.output)
        await engine.shutdown()

    asyncio.run(_run())


@app.command()
def calc(
    expression: str = typer.Argument(..., help="Arithmetic expression, e.g. 2+2*3"),
):
    """Run the calculator through the agent tool loop (MockLLM, no API key)."""

    async def _run():
        from aetherflow.core.tool_loop import run_tool_loop
        from aetherflow.integrations.llm.mock import MockLLMClient
        from aetherflow.tools.registry import ToolRegistry

        reg = ToolRegistry()
        await reg.load_builtins()
        out = await run_tool_loop(MockLLMClient(), reg, expression)
        console.print(str(out["answer"]))
        if out.get("steps", 0) < 1 or out.get("answer") is None:
            raise typer.Exit(code=1)

    asyncio.run(_run())


@app.command("list-tools")
def list_tools():
    async def _list():
        from aetherflow.tools.registry import ToolRegistry
        reg = ToolRegistry()
        await reg.load_builtins()
        table = Table(title="Built-in Tools")
        table.add_column("Name", style="cyan")
        for name in reg.list_tools():
            table.add_row(name)
        console.print(table)
    asyncio.run(_list())


@app.command()
def doctor():
    console.print("[bold]AetherFlow Doctor[/]\n")
    checks = [
        ("Python >= 3.11", True),
        ("pydantic", True),
        ("Config directory", True),
        ("LLM API keys", False),
    ]
    for name, ok in checks:
        status = "[green]✓[/]" if ok else "[yellow]⚠[/]"
        console.print(f"  {status}  {name}")
    console.print("\n[dim]Note: This is a diagnostic stub.[/]")


if __name__ == "__main__":
    app()
