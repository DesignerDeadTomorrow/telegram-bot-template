from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.infrastructure.config import Settings
from src.infrastructure.database.client import DatabaseClient


class DatabaseProvider(Provider):
    """DI для базы данных."""

    @provide(scope=Scope.APP)
    async def client(self, settings: Settings) -> AsyncIterable[DatabaseClient]:
        """Запуск базы данных 1 раз на весь проект."""

        client = DatabaseClient(
            url=settings.database.url,
            pool_size=20,
            max_overflow=30,
        )

        await client.connect()
        yield client
        await client.close()

    @provide(scope=Scope.REQUEST)
    async def session(self, client: DatabaseClient) -> AsyncIterable[AsyncSession]:
        """Открытие сессии базы данных на 1 запрос."""

        async with client.session_factory() as session:
            yield session
