import asyncio
import logging
from config_reader import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())