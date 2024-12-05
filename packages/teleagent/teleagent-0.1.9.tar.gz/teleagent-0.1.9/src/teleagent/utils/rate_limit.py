import abc
import math
import time
import typing as tp
from contextlib import asynccontextmanager
from datetime import timedelta

from teleagent.utils import delay

try:
    from redis.asyncio import Redis
except ImportError:
    Redis = None  # type: ignore[misc,assignment]

__all__ = [
    "RateLimitMemory",
    "RateLimitRedis",
    "AccountRateLimitHandler",
]


class RateLimit(abc.ABC):
    def __init__(self, function_name: str, ex_time: int | timedelta, **kwargs: tp.Any) -> None:
        self._function_name = function_name

        if isinstance(ex_time, timedelta):
            self._ex_time = int(ex_time.total_seconds())
        else:
            self._ex_time = ex_time

    @abc.abstractmethod
    async def set(self, slug: str) -> None:
        pass

    @abc.abstractmethod
    async def get_seconds(self, slug: str) -> int | None:
        pass


class RateLimitMemory(RateLimit):
    def __init__(self, *args: tp.Any, **kwargs: tp.Any) -> None:
        super().__init__(*args, **kwargs)

        self._storage: dict[str, float] = {}

    async def set(self, slug: str) -> None:
        expires_at = time.time() + self._ex_time
        self._storage[slug] = expires_at

    async def get_seconds(self, slug: str) -> int | None:
        current_time = time.time()
        expires_at = self._storage.get(slug)

        if expires_at is None:
            return None

        if current_time > expires_at:
            del self._storage[slug]
            return None

        return math.ceil(expires_at - current_time)


class RateLimitRedis(RateLimit):
    _key_prefix: str = "rate_limit"

    def __init__(self, *args: tp.Any, redis_client: Redis, **kwargs: tp.Any) -> None:
        super().__init__(*args, **kwargs)

        self._redis_client = redis_client

    async def set(self, slug: str) -> None:
        await self._redis_client.set(self._build_key(slug), 0, ex=self._ex_time)

    async def get_seconds(self, slug: str) -> int | None:
        ttl = await self._redis_client.ttl(self._build_key(slug))
        return ttl if ttl > 0 else None

    def _build_key(self, slug: str) -> str:
        return f"{self._key_prefix}:{self._function_name}:{slug}"


class AccountRateLimitHandler:
    def __init__(self, account_id: int) -> None:
        self._slug = str(account_id)

    @asynccontextmanager
    async def handle(self, rate_limit: RateLimit) -> tp.AsyncGenerator[None, None]:
        seconds = await rate_limit.get_seconds(self._slug)
        if seconds is not None:
            await delay(seconds)

        try:
            yield
        finally:
            await rate_limit.set(self._slug)
