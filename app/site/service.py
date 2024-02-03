from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from .services.database import inject as inject_database
from .services.scheduler import inject as inject_scheduler, ScheulerType
from .services.memcache import inject as inject_memcache, Memcache


DatabaseService = Annotated[Session, Depends(inject_database)]
SchedulerService = Annotated[ScheulerType, Depends(inject_scheduler)]
MemcacheService = Annotated[type[Memcache], Depends(inject_memcache)]
