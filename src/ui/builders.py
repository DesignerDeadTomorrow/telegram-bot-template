from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def inline_menu_builder(
    content_btns: list[InlineKeyboardButton] | None = None,
    nav_btns: list[InlineKeyboardButton] | None = None,
    back_btns: list[InlineKeyboardButton] | None = None,
    content_adjust: int = 1,
    nav_adjust: int = 2,
    back_adjust: int = 1,
) -> InlineKeyboardMarkup:
    """
    Сборщик inline клавиатур под любые сценарии

    Args:
        content_btns: Список кнопок основного контента клавиатуры
        nav_btns: Список кнопок навигации по клавиатуре (◀️▶️)
        back_btns: Список кнопок для перемещения по меню (⏪ Главное меню)
        content_adjust: Размер сетки для кнопок контента
        nav_adjust: Размер сетки для кнопок навигации
        back_adjust: Размер сетки для кнопок перемещения

    Returns:
        InlineKeyboardMarkup: Inline клавиатура
    """

    keyboard = InlineKeyboardBuilder()

    if content_btns:
        keyboard.row(*content_btns, width=content_adjust)

    if nav_btns:
        keyboard.row(*nav_btns, width=nav_adjust)

    if back_btns:
        keyboard.row(*back_btns, width=back_adjust)

    return keyboard.as_markup()


def reply_menu_builder(
    btns: list[KeyboardButton],
    adjust: int = 2,
    resize_keyboard: bool = True,
    one_time_keyboard: bool = False,
    input_field_placeholder: str | None = None,
    is_persistent: bool = False,
    selective: bool = False,
) -> ReplyKeyboardMarkup:
    """
    Сборщик reply клавиатур под любые сценарии

    Args:
        btns: Список кнопок клавиатуры
        adjust: Размер сетки клавиатуры
        resize_keyboard: Уменьшить клавиатуру до компактного размера
        one_time_keyboard: Скрывать клавиатуру после нажатия на любую кнопку
        input_field_placeholder: Текст-подсказка внутри поля ввода сообщения
        is_persistent: Всегда показывать клавиатуру на экране
        selective: Показывать клавиатуру только конкретному пользователю


    Returns:
        ReplyKeyboardMarkup: Reply клавиатура
    """

    keyboard = ReplyKeyboardBuilder()

    keyboard.row(*btns).adjust(adjust)

    return keyboard.as_markup(
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        is_persistent=is_persistent,
        selective=selective,
    )
