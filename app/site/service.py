from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from .services.database import inject as inject_database
from .services.scheduler import inject as inject_scheduler, ScheulerType
from .services.simple_cache import inject as inject_memcache, SimpleCache
from .services.template import inject as inject_template, Jinja2Templates


DatabaseService = Annotated[Session, Depends(inject_database)]
SchedulerService = Annotated[ScheulerType, Depends(inject_scheduler)]
MemcacheService = Annotated[type[SimpleCache], Depends(inject_memcache)]
TemplateService = Annotated[Jinja2Templates, Depends(inject_template)]
