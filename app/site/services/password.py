from typing import Optional
from passlib.context import CryptContext


_pwd_context: Optional[CryptContext] = None


def initialize() -> None:
    global _pwd_context
    if _pwd_context is not None:
        return
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def inject() -> CryptContext:
    global _pwd_context
    if _pwd_context is None:
        raise RuntimeError("Password context not initialized")
    return _pwd_context
