from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello")