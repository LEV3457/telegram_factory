from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
logger.info("Бот создан")
dp = Dispatcher()
logger.info("Диспетчер создан")


# Создаем клавиатуру
def get_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="json", callback_data="btn1"),
            InlineKeyboardButton(text="txt", callback_data="btn2"),
            InlineKeyboardButton(text="CSV", callback_data="btn3"),

        ]
    ])
    return keyboard


# Альтернативный вариант (динамическое добавление кнопок)
def get_inline_keyboard_alt() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="Кнопка 1", callback_data="btn1"),
        InlineKeyboardButton(text="Кнопка 2", callback_data="btn2"),
        InlineKeyboardButton(text="Кнопка 3", callback_data="btn3"),
    )


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Вот инлайн-клавиатура: выберите знак для счета",
        reply_markup=get_inline_keyboard()  # или get_inline_keyboard_alt()
    )


# Обработчик нажатий на кнопки
@dp.callback_query(lambda callback: callback.data.startswith("btn"))
async def handle_button_click(callback: types.CallbackQuery):
    btn_data = callback.data
    if btn_data == "btn1":
        await callback.answer("Вы нажали на (json)", show_alert=True)
    elif btn_data == "btn2":
        await callback.answer("Вы нажали на  (txt)", show_alert=True)
    elif btn_data == "btn3":
        await callback.answer("Вы нажали на  (CSV)", show_alert=True)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
