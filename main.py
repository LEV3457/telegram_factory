import asyncio
import os
import time
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from abc import ABC, abstractmethod
import json
import csv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
logger.info("Бот создан")
dp = Dispatcher()
logger.info("Диспетчер создан")

class Document(ABC):
    @abstractmethod
    def save(self, filename: str, data: dict) -> str:
        pass

class TXTDocument(Document):
    def save(self, filename: str, data: dict) -> str:
        filepath = f"{filename}.txt"
        with open(filepath, "w", encoding="UTF-8") as file:
            file.write(data["message_text"])
        return filepath

class JSONDocument(Document):
    def save(self, filename: str, data: dict) -> str:
        filepath = f"{filename}.json"
        with open(filepath, "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return filepath

class CSVDocument(Document):
    def save(self, filename: str, data: dict) -> str:
        filepath = f"{filename}.csv"
        with open(filepath, "w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(["message_id", "message_text"])
            writer.writerow([data["message_id"], data["message_text"]])
        return filepath

class DocumentFactory:
    @staticmethod
    def create_document(doc_type: str) -> Document:
        doc_type = doc_type.lower()
        if doc_type == "txt":
            return TXTDocument()
        elif doc_type == "json":
            return JSONDocument()
        elif doc_type == "csv":
            return CSVDocument()
        else:
            raise ValueError(f"Неизвестный тип файла: {doc_type}")

def get_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="JSON", callback_data="export_json"),
            InlineKeyboardButton(text="TXT", callback_data="export_txt"),
            InlineKeyboardButton(text="CSV", callback_data="export_csv"),
        ]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer("Привет! Я помогу с форматами документов!")
    data = {"name": "Silvestr", "last name": "Stallone", "film": "Rocky"}
    await message.answer("Мои команды: /start")
    await message.answer(
        " Вот инлайн-клавиатура: выберите  сообщение для экспорта",
        reply_markup=get_inline_keyboard()
    )

user_messages = {}

@dp.message()
async def save_user_message(message: types.Message):
    user_messages[message.from_user.id] = {
        "message_id": message.message_id,
        "message_text": message.text or message.caption or "Нет текста:("
    }
    await message.answer(
        " Выберите формат экспорта:",
        reply_markup=get_inline_keyboard()
    )

@dp.callback_query(lambda callback: callback.data.startswith("export_"))
async def handle_button_click(callback: types.CallbackQuery):
    btn_data = callback.data.split('_')[1].lower()
    user_id = callback.from_user.id
    
    if user_id not in user_messages:
        await callback.answer("Сначала отправьте сообщение ", show_alert=True)
        return
    
    message_data = user_messages[user_id]
    
    try:
        # Создаем экспортер и сохраняем файл
        exporter = DocumentFactory.create_document(btn_data)
        filename = f"export_{user_id}_{int(time.time())}"
        filepath = exporter.save(filename, message_data)
        
        # Читаем файл и отправляем в Telegram
        with open(filepath, "rb") as file:
            file_data = file.read()
        
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=BufferedInputFile(file_data, filename=f"message_export.{btn_data}"),
            caption=f"📁 Экспорт сообщения ({btn_data.upper()})"
        )
        
        # Удаляем временный файл
        os.remove(filepath)
        await callback.answer("Файл успешно экспортирован, скажи круто:)")
        
    except ValueError as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)
    except Exception as e:
        logger.error(f"Export error: {e}")
        await callback.answer("Ошибка при экспорте файла", show_alert=True)
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

async def main():
    logger.add('bot.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation="1 MB",
               retention="3 days",
               backtrace=True,
               diagnose=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())