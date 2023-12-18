from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Any
from fastapi import Depends


_engine: Optional[Engine] = None

def initialize(connection_string: str, args: Any = None):
    global _engine
    if _engine is not None:
        return
    _engine = create_engine(connection_string, connect_args=args)


def inject_db_session() -> Session:
    global _engine
    if _engine is None:
        raise RuntimeError("Database engine is not initialized")
    try:
        session = Session(bind=_engine)
        yield session
    finally:
        session.close()


def require_db_session() -> Session:
    global _engine
    if _engine is None:
        raise RuntimeError("Database engine is not initialized")
    return Session(bind=_engine)


SessionD = Annotated[Session, Depends(inject_db_session)]