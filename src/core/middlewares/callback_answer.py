from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, TelegramObject


class AutoCallbackAnswerMiddleware(BaseMiddleware):
    """Мидлвейр для автоматического callback.answer."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[TelegramObject]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> TelegramObject:
        if isinstance(event, CallbackQuery):
            try:
                return await handler(event, data)
            finally:
                try:
                    await event.answer()
                except TelegramBadRequest:
                    pass

        return await handler(event, data)
