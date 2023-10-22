from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_row_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🩺 Запись на приём 🕑", callback_data="appointment")],
        [InlineKeyboardButton(text="🖌 Мои записи 🗒", callback_data="my_notes")],
        [InlineKeyboardButton(text="💉 Мои анализы 🧪", callback_data="my_tests")],
        [InlineKeyboardButton(text="🦠 Симптомы 🤢", callback_data="symptoms")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)