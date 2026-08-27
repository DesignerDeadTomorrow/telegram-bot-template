from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, TelegramObject


class ChatTypeFilter(BaseFilter):
    """Фильтр для проверки чата на конкретный тип."""

    def __init__(self, *chat_type: ChatType | str) -> None:
        self.chat_type = set(chat_type)

    async def __call__(self, event: TelegramObject) -> bool:
        if isinstance(event, CallbackQuery):
            message = getattr(event, "message", None)

            if message is None:
                return False

            chat = getattr(message, "chat", None)

        else:
            chat = getattr(event, "chat", None)

        if chat is None:
            return False

        return chat.type in self.chat_type
