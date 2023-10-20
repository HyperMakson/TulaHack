from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Запись на приём", callback_data="appointment")],
        [InlineKeyboardButton(text="Мои записи", callback_data="my_notes")],
        [InlineKeyboardButton(text="Мои анализы", callback_data="my_tests")],
        [InlineKeyboardButton(text="Симптомы", callback_data="symptoms")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Здравствуйте! Вы попали", reply_markup=keyboard)

@router.callback_query(F.data == "appointment")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это запись")
    await callback.answer()

@router.callback_query(F.data == "my_notes")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это мои записи")
    await callback.answer()

@router.callback_query(F.data == "my_tests")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это мои анализы")
    await callback.answer()

@router.callback_query(F.data == "symptoms")
async def start_appointment(callback: CallbackQuery):
    await callback.message.answer("Это симптомы")
    await callback.answer()