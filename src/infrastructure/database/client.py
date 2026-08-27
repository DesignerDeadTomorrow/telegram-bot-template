from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.infrastructure.database.base import BaseORM


class DatabaseClient:
    """Клиент для базы данных."""

    def __init__(
        self,
        url: str,
        echo: bool = False,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 300,
        pool_timeout: int = 30,
    ) -> None:
        # параметры
        self.url = url
        self._echo = echo
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._pool_recycle = pool_recycle
        self._pool_timeout = pool_timeout

        # клиент
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        """Создание соединенние с базой данных."""

        if self._engine:
            return

        self._engine = create_async_engine(
            url=self.url,
            pool_size=self._pool_size,
            max_overflow=self._max_overflow,
            pool_recycle=self._pool_recycle,
            pool_timeout=self._pool_timeout,
            echo=self._echo,
            pool_pre_ping=True,
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with self._engine.begin() as conn:
            await conn.run_sync(BaseORM.metadata.create_all)

    async def close(self) -> None:
        """Закрытие соединения с базой данных."""

        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Получение фабрики соединений с базой данных."""

        if self._session_factory is None:
            raise RuntimeError(
                "Вы забыли инициализировать базу данных перед её работой. Сначала вызовите .connect() в начале работы проекта."
            )

        return self._session_factory
