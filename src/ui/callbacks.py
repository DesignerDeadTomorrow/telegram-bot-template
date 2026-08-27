from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class NavActionEnum(StrEnum):
    """
    Каждая константа приводит к определённому разделу интерфеса.

    Attributes:
        START (str): Путь до главного меню.
        ADMIN (str): Путь до админ меню.
    """

    START = "start"
    ADMIN = "admin"


class NavCD(CallbackData, prefix="nav"):
    """
    Callback для перемещения по меню.

    Attributes:
        action (NavActionEnum): Место куда переместиться в меню (в главное меню, в админ меню и тд).
    """

    action: NavActionEnum
