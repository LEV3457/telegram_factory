from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

# Ваш оригинальный код классов документов (оставлен без изменений)
from abc import ABC, abstractmethod
import json
import csv

class Document(ABC):
    @abstractmethod
    def save(self, filename: str, data: dict) -> None:
        pass

class TXTDocument(Document):
    def save(self, filename: str, data: dict) -> None:
        with open(f"{filename}.txt", "w", encoding="UTF-8") as file:
            for key, value in data.items():
                file.write(f"{key}: {value}\n")

class JSONDocument(Document):
    def save(self, filename: str, data: dict) -> None:
        with open(f"{filename}.json", "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

class CSVDocument(Document):
    def save(self, filename: str, data: dict) -> None:
        with open(f"{filename}.csv", "w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerow(data.values())

class DocumentFactory:
    @staticmethod
    def create_document(doc_type: str) -> Document:
        if doc_type == "txt":
            return TXTDocument()
        elif doc_type == "json":
            return JSONDocument()
        elif doc_type == "csv":
            return CSVDocument()
        else:
            raise ValueError("Неизвестный тип файла.")
# Конец вашего оригинального кода

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

# Пример данных для экспорта (можно заменить на получение от пользователя)
SAMPLE_DATA = {
    "name": "Иван Иванов",
    "age": "30",
    "email": "ivan@example.com"
}

def get_export_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Экспорт в JSON", callback_data="export_json"),
            InlineKeyboardButton(text="Экспорт в TXT", callback_data="export_txt"),
            InlineKeyboardButton(text="Экспорт в CSV", callback_data="export_csv")
        ]
    ])

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Выберите формат для экспорта данных:",
        reply_markup=get_export_keyboard()
    )

@dp.callback_query(lambda c: c.data.startswith("export_"))
async def process_export(callback: types.CallbackQuery):
    format_type = callback.data.split("_")[1]  # получаем json/txt/csv
    
    try:
        # Используем ваш DocumentFactory
        exporter = DocumentFactory.create_document(format_type)
        filename = f"export_{callback.from_user.id}"
        exporter.save(filename, SAMPLE_DATA)
        
        # Отправляем файл пользователю
        with open(f"{filename}.{format_type}", "rb") as