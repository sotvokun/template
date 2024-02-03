from typing import Optional, Any, TypedDict, Unpack
from datetime import datetime

from sqlalchemy.util import inject_docstring_text


class MemcacheGettingOption(TypedDict):
    force: bool


class Memcache:
    _memcache: dict[str, Any] = {}
    _memcache_expires: dict[str, int] = {}


    @staticmethod
    def _now() -> int:
        """
        Get the current timestamp with millisecond
        """
        return int(datetime.now().timestamp() * 1000)


    @staticmethod
    def is_expired(key: str) -> bool:
        """
        Check if the key is expired
        """
        if key not in Memcache._memcache_expires:
            return True
        return Memcache._now() > Memcache._memcache_expires[key]


    @staticmethod
    def get[T](
        key: str,
        default: Optional[T] = None,
        /,
        **options: Unpack[MemcacheGettingOption]
    ) -> Optional[T]:
        """
        Get the value from the memcache
        ---
        key `str`
            The key to get the value

        default `Optional[T]`
            The default value if the key is not found

        options `**`
            force `bool`
                Force to get the value from the memcache even if it's expired
        """
        if key in Memcache._memcache:
            value = Memcache._memcache[key]
            if options.get("force", False):
                return value
            return default if Memcache.is_expired(key) else value
        else:
            return default


    @staticmethod
    def set(key: str, value: Any, lifetime_ms: Optional[int] = None) -> None:
        """
        Set the value to the memcache
        ---
        key `str`
            The key to set the value

        value `Any`
            The value to set

        lifetime_ms `Optional[int]`
            The lifetime of the value in millisecond
        """
        Memcache._memcache[key] = value
        if lifetime_ms is not None:
            Memcache._memcache_expires[key] = Memcache._now() + lifetime_ms


    @staticmethod
    def delete(key: str) -> None:
        """
        Delete the value from the memcache
        """
        if key in Memcache._memcache:
            del Memcache._memcache[key]
        if key in Memcache._memcache_expires:
            del Memcache._memcache_expires[key]


def inject() -> type[Memcache]:
    return Memcache
