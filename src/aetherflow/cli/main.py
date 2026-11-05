"""
Entry point for the `aetherflow` command.
"""

from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="aetherflow",
    help="AetherFlow: multi-agent orchestration from the command line",
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
    """Tiny JSON API: POST /run {"goal": "..."} -> TaskResult. GET /health."""
    import json
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from aetherflow import AetherEngine

    engine = AetherEngine.from_config(config) if config else AetherEngine.from_env()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(engine.initialize())

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: dict) -> None:
            data = json.dumps(body, default=str).encode()
            self.send_response(code)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/health":
                self._send(200, {"ok": True})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/run":
                return self._send(404, {"error": "not found"})
            try:
                n = int(self.headers.get("content-length", 0))
                goal = json.loads(self.rfile.read(n) or b"{}")["goal"]
            except (ValueError, KeyError):
                return self._send(400, {"error": "expected {\"goal\": str}"})
            # one event loop shared by all requests; runs are serialized
            result = asyncio.run_coroutine_threadsafe(engine.run_goal(goal), loop)
            self._send(200, result.result().model_dump(mode="json"))

        def log_message(self, fmt, *args):
            console.print(f"[dim]{self.address_string()} {fmt % args}[/]")

    import threading

    threading.Thread(target=loop.run_forever, daemon=True).start()
    console.print(f"listening on http://{host}:{port}")
    try:
        ThreadingHTTPServer((host, port), Handler).serve_forever()
    except KeyboardInterrupt:
        pass


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
    import importlib.util
    import os
    import sys
    from pathlib import Path

    checks = [
        ("python >= 3.11", sys.version_info >= (3, 11)),
        ("pydantic installed", importlib.util.find_spec("pydantic") is not None),
        ("configs/ directory", Path("configs").is_dir()),
        (
            "LLM API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)",
            bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")),
        ),
    ]
    for name, ok in checks:
        status = "[green]ok[/]     " if ok else "[yellow]missing[/]"
        console.print(f"  {status} {name}")
    if not checks[-1][1]:
        console.print("\n[dim]no key set, agents will use the offline mock LLM[/]")


if __name__ == "__main__":
    app()
