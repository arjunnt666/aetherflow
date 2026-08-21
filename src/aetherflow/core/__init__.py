from aetherflow.core.types import *  # noqa: F401,F403

__all__ = ["AetherEngine", "AetherConfig", "AgentConfig"]


def __getattr__(name: str):
    if name == "AetherEngine":
        from aetherflow.core.engine import AetherEngine

        return AetherEngine
    if name in ("AetherConfig", "AgentConfig"):
        from aetherflow.core import config as cfg

        return getattr(cfg, name)
    raise AttributeError(name)
