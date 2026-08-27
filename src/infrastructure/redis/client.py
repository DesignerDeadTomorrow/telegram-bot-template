from json import JSONDecodeError, dumps, loads
from typing import Any

from pydantic import BaseModel
from redis.asyncio import ConnectionPool, Redis


class RedisClient:
    """Клиент для редиса."""

    def __init__(
        self,
        url: str,
        max_connections: int = 20,
        socket_connect_timeout: float = 5.0,
        retry_on_timeout: bool = True,
        health_check_interval: int = 30,
    ) -> None:
        # параметры
        self.url = url
        self._max_connections = max_connections
        self._socket_connect_timeout = socket_connect_timeout
        self._retry_on_timeout = retry_on_timeout
        self._health_check_interval = health_check_interval

        # клиент
        self._redis: Redis | None = None
        self._pool: ConnectionPool | None = None

    async def connect(self) -> None:
        """Создание соединенние с редисом."""

        if self._redis:
            return

        self._pool = ConnectionPool.from_url(
            url=self.url,
            max_connections=self._max_connections,
            socket_connect_timeout=self._socket_connect_timeout,
            retry_on_timeout=self._retry_on_timeout,
            decode_responses=True,
            health_check_interval=self._health_check_interval,
        )

        self._redis = Redis(connection_pool=self._pool)

    async def close(self) -> None:
        """Закрытие соединения с редисом."""

        if self._redis:
            await self._redis.aclose()
            self._redis = None

        if self._pool:
            await self._pool.disconnect()
            self._pool = None

    @staticmethod
    def fullkey(prefix: str, key: str | int) -> str:
        """
        Создание полного ключа для кэширования.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.

        Returns:
            str: Полный ключ.
        """

        return f"{prefix}:{key}"

    async def set(
        self,
        prefix: str,
        key: str | int,
        value: Any,
        ex: int,
        nx=False,
    ) -> bool:
        """
        Кэширование данных в редис.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.
            value: Данные, которые будут кэшироваться.
            ex: Время жизни кэша (в секундах).
            nx: Если True, запись произойдёт только, если отсутствует запись под таким ключём.

        Returns:
            bool: Были ли данные закэшированы.
        """

        fullkey = self.fullkey(prefix=prefix, key=key)

        if isinstance(value, BaseModel):
            value = value.model_dump_json()

        elif isinstance(value, (dict, list)):
            value = dumps(value, default=str)

        return bool(await self.client.set(name=fullkey, value=value, ex=ex, nx=nx))

    async def get(self, prefix: str, key: str | int) -> Any:
        """
        Получение данных из кэша редиса.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.

        Returns:
            Any: Данные после парсинга из кэша в их вид при кэшировании.
        """

        fullkey = self.fullkey(prefix=prefix, key=key)

        cache = await self.client.get(name=fullkey)

        if cache is None:
            return None

        if cache.startswith(("{", "[")):
            try:
                return loads(cache)
            except (JSONDecodeError, TypeError):
                return cache

        return cache

    async def delete(
        self, prefix: str, keys: str | int | list[str | int], is_async: bool = False
    ) -> int:
        """
        Удаление кэша.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            keys: Уникальная часть ключа или ключей.
            is_async: Удалять ли кэш асинхронно, True для огромных массивом.

        Returns:
            int: Количетсво удалённых данных из кэша.
        """

        keys_list = keys if isinstance(keys, list) else [keys]
        fullkeys = [self.fullkey(prefix=prefix, key=key) for key in keys_list]

        if not fullkeys:
            return 0

        if is_async:
            return await self.client.unlink(*fullkeys)
        else:
            return await self.client.delete(*fullkeys)

    async def incr(self, prefix: str, key: str | int) -> int:
        """
        Кэширование числа и его увеличение на 1.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.

        Returns:
            int: Число в кэше.
        """

        fullkey = self.fullkey(prefix=prefix, key=key)

        return await self.client.incr(name=fullkey, amount=1)

    async def expire_ttl(self, prefix: str, key: str | int, ex: int = 300) -> bool:
        """
        Увеличение жизни кэша по ключу.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.
            ex: Время жизни кэша (в секундах).

        Returns:
            bool: Был ли ключ и был ли TTL продлён.
        """

        fullkey = self.fullkey(prefix=prefix, key=key)

        return await self.client.expire(name=fullkey, time=ex)

    async def incr_with_ttl(self, prefix: str, key: str | int, ex: int, nx=True) -> int:
        """
        Атомарное увелечение счетчика и установку времени жизни кэша.

        Args:
            prefix: Префикс ключа (например: cache, spam).
            key: Уникальная часть ключа.
            ex: Время жизни кэша (в секундах).
            nx: Если True, запись произойдёт только, если отсутствует запись под таким ключём.

        Returns:
            int: Число в кэше.
        """

        fullkey = self.fullkey(prefix=prefix, key=key)

        async with self.client.pipeline(transaction=True) as pipe:
            pipe.incr(name=fullkey)
            pipe.expire(name=fullkey, time=ex, nx=nx)
            result = await pipe.execute()

        return result[0]

    @property
    def client(self) -> Redis:
        """Получение редис соединения."""

        if not self._redis:
            raise RuntimeError(
                "Вы забыли инициализировать редис перед его работой. Сначала вызовите .connect()"
            )

        return self._redis
