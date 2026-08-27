from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject


class IsAdmin(BaseFilter):
    """Фильтр для проверки ID пользователя на ID админа."""

    def __init__(self, admin_ids: list[int] | None = None) -> None:
        self.admin_ids = admin_ids or []

    async def __call__(self, event: TelegramObject) -> bool:
        user = getattr(event, "from_user", None)

        if user is None:
            return False

        return user.id in self.admin_ids
