"""Simple role-based access control."""

from __future__ import annotations
from typing import Optional


class RBAC:
    def __init__(self):
        self._roles: dict[str, set[str]] = {
            "admin": {"*"},
            "operator": {"agent.run", "pipeline.run", "tool.call"},
            "viewer": {"agent.read", "pipeline.read", "metrics.read"},
        }
        self._user_roles: dict[str, set[str]] = {}

    def assign_role(self, user: str, role: str) -> None:
        self._user_roles.setdefault(user, set()).add(role)

    def check(self, user: str, permission: str) -> bool:
        roles = self._user_roles.get(user, set())
        for role in roles:
            perms = self._roles.get(role, set())
            if "*" in perms or permission in perms:
                return True
        return False
