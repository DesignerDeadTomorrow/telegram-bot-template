from typing import Any, Awaitable, Callable, Protocol

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class RedisClientProtocol(Protocol):
    async def incr_with_ttl(self, prefix: str, key: str | int, ex: int) -> int:
        pass


class ThrottlingMiddleware(BaseMiddleware):
    """Мидлвейр для анти-спама."""

    def __init__(
        self,
        redis: RedisClientProtocol,
        limit: int = 1,
        ex: int = 1,
        prefix: str = "spam",
    ) -> None:
        # параметры
        self._redis = redis
        self._limit = limit
        self._ex = ex
        self._prefix = prefix

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[TelegramObject]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> TelegramObject | None:
        user = getattr(event, "from_user", None)

        if user is None:
            return await handler(event, data)

        spam_count = await self._redis.incr_with_ttl(
            prefix=self._prefix, key=user.id, ex=self._ex
        )

        if spam_count > self._limit:
            return

        return await handler(event, data)
