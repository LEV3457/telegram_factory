from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
logger.info("Бот создан")
dp = Dispatcher()
logger.info("Диспетчер создан")


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я помогу с форматами документов!")
    data = {"name": "Silvestr", "last name": "Stallone", "film": "Rocky"}
    await message.answer("Мои команды: /start и /hello")
    logger.info("Бот запущен!")


@dp.message(Command("hello"))
async def hello(message: types.Message):
    await message.answer("Выбери формат документа!")
    logger.info("Бот рассказал свои функции")
