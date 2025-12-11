import os
import csv
import logging
from functools import wraps


class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


def logged(exception_type, mode="console", log_file=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if mode == "file":
                filename = log_file if log_file else "operations.txt"
                handler = logging.FileHandler("operations.txt", encoding="utf-8")
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)

            if not logger.handlers:
                logger.addHandler(handler)

            try:
                logger.info(f"Запуск методу {func.__name__}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} виконано успішно")
                return result

            except exception_type as e:
                logger.error(f"Помилка у {func.__name__}: {e}")
                raise e

        return wrapper
    return decorator


class CSVFileManager:
    def __init__(self, filepath, delimiter=";"):
        self.filepath = filepath
        self.delimiter = delimiter

        if not os.path.exists(self.filepath):
            raise FileNotFound(f"Файл '{self.filepath}' не існує")

    @logged(FileCorrupted, mode="file", log_file="example.txt")
    def read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return list(csv.reader(f, delimiter=self.delimiter))
        except Exception as e:
            raise FileCorrupted(f"Помилка читання: {e}")

    @logged(FileCorrupted, mode="file")
    def write(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=self.delimiter)
                writer.writerows(data)
        except Exception as e:
            raise FileCorrupted(f"Помилка запису: {e}")

    @logged(FileCorrupted, mode="file")
    def append(self, data):
        try:
            with open(self.filepath, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=self.delimiter)
                writer.writerows(data)
        except Exception as e:
            raise FileCorrupted(f"Помилка дописування: {e}")


if __name__ == "__main__":
    manager = CSVFileManager("products.csv")

    manager.write([
        ["Product", "Price"],
        ["Apple", 10],
        ["Banana", 20]
    ])

    print("Файл містить:", manager.read())

    manager.append([
        ["Orange", 30],
        ["Milk", 40]
    ])

    print("Після дописування:", manager.read())
