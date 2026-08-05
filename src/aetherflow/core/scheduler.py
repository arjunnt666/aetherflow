"""
Scheduler — handles cron triggers, event-based triggers, and delayed tasks.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable, Optional
from uuid import uuid4

logger = logging.getLogger("aetherflow.scheduler")


class ScheduledJob:
    def __init__(self, job_id: str, name: str, trigger: str, callback: Callable, enabled: bool = True):
        self.job_id = job_id
        self.name = name
        self.trigger = trigger
        self.callback = callback
        self.enabled = enabled
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0


class Scheduler:
    def __init__(self):
        self._jobs: dict[str, ScheduledJob] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    def add_job(self, name: str, trigger: str, callback: Callable, job_id: Optional[str] = None) -> str:
        jid = job_id or f"job-{uuid4().hex[:8]}"
        self._jobs[jid] = ScheduledJob(jid, name, trigger, callback)
        logger.info(f"Scheduled job '{name}' ({trigger})")
        return jid

    def remove_job(self, job_id: str) -> None:
        self._jobs.pop(job_id, None)

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("Scheduler started")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("Scheduler stopped")

    async def _loop(self) -> None:
        while self._running:
            await asyncio.sleep(30)
