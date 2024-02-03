from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, Callable


_engine: Optional[Engine] = None


def initialize(url: str, **kwargs):
    """
    Initialize the database engine
    """
    global _engine
    if _engine is not None:
        return
    _engine = create_engine(url, **kwargs)


def inject():
    global _engine
    if _engine is None:
        raise RuntimeError("Database engine is not initialized")
    session: Optional[Session] = None
    try:
        session = sessionmaker(bind=_engine)()
        yield session
    finally:
        if session is not None:
            session.close()


def require_session[T](fn: Callable[[Session], T]) -> T:
    global _engine
    if _engine is None:
        raise RuntimeError("Database engine is not initialized")
    session = sessionmaker(bind=_engine)()
    result = fn(session)
    session.close()
    return result
