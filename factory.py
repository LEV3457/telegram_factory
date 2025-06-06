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