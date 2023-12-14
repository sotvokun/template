from typing import Optional, Annotated
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends


_scheduler: Optional[AsyncIOScheduler] = None

def initialize_scheduler():
    global _scheduler
    _scheduler = AsyncIOScheduler()


def inject_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        raise RuntimeError("Scheduler is not initialized")
    return _scheduler


SchedulerD = Annotated(AsyncIOScheduler, Depends(inject_scheduler))