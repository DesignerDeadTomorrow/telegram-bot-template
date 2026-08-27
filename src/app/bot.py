from asyncio import run as async_run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from dishka.integrations.aiogram import setup_dishka as setup_dishka_aiogram
from dishka.integrations.taskiq import setup_dishka as setup_dishka_taskiq

from src.app.di import create_container
from src.core import AutoCallbackAnswerMiddleware, ThrottlingMiddleware
from src.infrastructure import RedisClient, broker, settings
from src.modules import router


async def on_startup(bot: Bot) -> None:
    """Действия при старте бота."""

    await bot.delete_webhook(drop_pending_updates=True)
    await broker.startup()


async def on_shutdown() -> None:
    """Действия при остановке бота."""

    await broker.shutdown()


async def main() -> None:
    """Сборка бота."""

    # бот и диспетчер
    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=RedisStorage.from_url(url=settings.redis.url))

    # контейнер и клиенты из провайдеров
    container = create_container(settings=settings)
    redis_client = await container.get(RedisClient)

    # мидлвейры
    dp.callback_query.middleware(AutoCallbackAnswerMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware(redis=redis_client))
    dp.message.outer_middleware(ThrottlingMiddleware(redis=redis_client))

    # загрузка роутера
    dp.include_router(router)

    # запуск контейнеров в DI
    setup_dishka_aiogram(container=container, router=dp)
    setup_dishka_taskiq(container=container, broker=broker)

    # регистрация startup/shutdown
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

    finally:
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    async_run(main())
