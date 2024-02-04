from typing import Optional, Any, TypedDict, Unpack
from datetime import datetime


class SimpleCacheGettingOption(TypedDict):
    force: bool


class SimpleCache:
    _cache: dict[str, Any] = {}
    _cache_expires: dict[str, int] = {}


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
        if key not in SimpleCache._cache_expires:
            return True
        return SimpleCache._now() > SimpleCache._cache_expires[key]


    @staticmethod
    def get[T](
        key: str,
        default: Optional[T] = None,
        /,
        **options: Unpack[SimpleCacheGettingOption]
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
        if key in SimpleCache._cache:
            value = SimpleCache._cache[key]
            if options.get("force", False):
                return value
            return default if SimpleCache.is_expired(key) else value
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
        SimpleCache._cache[key] = value
        if lifetime_ms is not None:
            SimpleCache._cache_expires[key] = SimpleCache._now() + lifetime_ms


    @staticmethod
    def delete(key: str) -> None:
        """
        Delete the value from the memcache
        """
        if key in SimpleCache._cache:
            del SimpleCache._cache[key]
        if key in SimpleCache._cache_expires:
            del SimpleCache._cache_expires[key]


def inject() -> type[SimpleCache]:
    return SimpleCache
