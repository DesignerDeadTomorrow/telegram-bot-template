from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.ui.callbacks import NavActionEnum, NavCD


def back_to_start_menu_kb(btn_text: str = "⏪ Главное меню") -> InlineKeyboardMarkup:
    """
    Кнопка чтобы вернуться в главное меню
    
    Args:
        btn_text: Текст для кнопки
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=btn_text,
            callback_data=NavCD(
                action=NavActionEnum.START,
            ).pack(),
        )
    )

    return keyboard.as_markup()


def back_to_admin_menu_kb(btn_text: str = "⏪ Админ меню") -> InlineKeyboardMarkup:
    """
    Кнопка чтобы вернуться в админ меню
    
    Args:
        btn_text: Текст для кнопки
    """

    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=btn_text,
            callback_data=NavCD(
                action=NavActionEnum.ADMIN,
            ).pack(),
        )
    )

    return keyboard.as_markup()
