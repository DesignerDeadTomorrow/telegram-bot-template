from dishka import AsyncContainer, make_async_container

from src.infrastructure import DatabaseProvider, RedisProvider, Settings


def create_container(settings: Settings) -> AsyncContainer:
    """
    Создание DI контейнера.

    Args:
        settings: Конфиг настроек для провайдеров (database, redis).

    Returns:
        AsyncContainer: Готовый асинхронный контейнер DI.
    """

    return make_async_container(
        RedisProvider(),
        DatabaseProvider(),
        context={Settings: settings},
    )
