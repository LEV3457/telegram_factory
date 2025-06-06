import asyncio
import os
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation="3 days",
               backtrace=True,
               diagnose=True)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    logger.info("Бот запущен!")

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.answer("Приветствие")
        logger.info('Бот ответил на команду /start')

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
