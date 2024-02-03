from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler


_scheduler: Optional[AsyncIOScheduler] = None


ScheulerType = AsyncIOScheduler


def initialize():
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = AsyncIOScheduler()


def inject() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        raise RuntimeError("Scheduler is not initialized")
    return _scheduler
