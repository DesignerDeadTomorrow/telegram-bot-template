from typing import AsyncIterable

from dishka import Provider, Scope, provide

from src.infrastructure.config import Settings
from src.infrastructure.redis.client import RedisClient


class RedisProvider(Provider):
    """DI для редиса."""

    @provide(scope=Scope.APP)
    async def client(self, settings: Settings) -> AsyncIterable[RedisClient]:
        """Запуск редиса 1 раз на весь проект."""

        client = RedisClient(url=settings.redis.url)

        await client.connect()
        yield client
        await client.close()
