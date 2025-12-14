import os
import csv
import logging
from functools import wraps
from typing import Callable, Any, Type, Optional, List


class FileNotFound(Exception):
    def __init__(self, filepath):
        super().__init__(f"Файл '{filepath}' не існує.")


class FileCorrupted(Exception):
    def __init__(self, message):
        super().__init__(message)


def logged(
    exception_type: Type[Exception],
    mode: str = "console",
    log_file: Optional[str] = None
) -> Callable:

    def decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if mode == "file":
                filename = log_file if log_file else "operations.txt"
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
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
                raise exception_type(str(e)) from e

        return wrapper

    return decorator


class CSVFileManager:
    def __init__(self, filepath: str, delimiter: str = ";"):
        self.filepath = filepath
        self.delimiter = delimiter

    @logged(FileCorrupted, mode="file", log_file="example.txt")
    def read(self) -> List[List[Any]]:
        if not os.path.exists(self.filepath):
            raise FileNotFound(self.filepath)

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return list(csv.reader(f, delimiter=self.delimiter))
        except (IOError, OSError, csv.Error) as e:
            raise FileCorrupted(f"Помилка читання: {e}") from e

    @logged(FileCorrupted, mode="file")
    def write(self, data: List[List[Any]]):
        try:
            with open(self.filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=self.delimiter)
                writer.writerows(data)
        except (IOError, OSError, csv.Error) as e:
            raise FileCorrupted(f"Помилка запису: {e}") from e

    @logged(FileCorrupted, mode="file")
    def append(self, data: List[List[Any]]):
        try:
            with open(self.filepath, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=self.delimiter)
                writer.writerows(data)
        except (IOError, OSError, csv.Error) as e:
            raise FileCorrupted(f"Помилка дописування: {e}") from e


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
