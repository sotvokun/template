from typing import Optional, Annotated, Any
from redis import Redis
from fastapi import Depends

from app.util import config

class RedisWrapper:
    def __init__(self, redis: Redis, **kwargs):
        self.redis = redis
        self.prefix = kwargs.get("prefix", "")

    def _wrap_key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    def raw(self) -> Redis:
        return self.redis

    def get(self, key: str, default: Optional[str]) -> Optional[str]:
        val = self.redis.get(self._wrap_key(key))
        if val is None:
            return default
        return str(val, encoding="utf-8")

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        self.redis.set(self._wrap_key(key), value, ex=expire)

    def delete(self, key: str) -> None:
        self.redis.delete(self._wrap_key(key))


_redis: Optional[Redis] = None


def initialize(connection_string: str):
    global _redis
    if _redis is not None:
        return
    _redis: Redis = Redis.from_url(connection_string)


def inject_redis() -> RedisWrapper:
    if _redis is None:
        raise RuntimeError("Redis is not initialized")
    prefix = config("redis.prefix", "")
    return RedisWrapper(_redis, prefix=prefix)


RedisD = Annotated[RedisWrapper, Depends(inject_redis)]