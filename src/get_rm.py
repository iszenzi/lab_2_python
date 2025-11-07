import os
import logging
import shutil
from src.exceptions import (
    EmptyPathError,
    UnknownFlagError,
    TooManyArgumentsError,
    TooLittleArgumentsError,
    FileNotExistError,
    AccessError,
)


def rm(string: str) -> None:
    """
    Удаление указанного файла/каталога
    :param string: строка аргументов команды rm
    """
    try:
        # Проверка ввода пустого пути
        if not string:
            raise EmptyPathError("Вы не ввели путь к файлу")

        parts = string.split()

        # Флаг рекурсивного удаления
        recursion = False
        path = None

        # Обработка аргументов
        for part in parts:
            if part == "-r":
                recursion = True
            elif path is None:
                path = part
            else:
                if part.startswith("-"):
                    raise UnknownFlagError(f"Неизвестный флаг '{part}'")
                else:
                    raise TooManyArgumentsError("Cлишком много аргументов")

        if path is None:
            raise EmptyPathError("Вы не ввели путь к файлу")

        ##Преобразование пути в абсолютный
        path = os.path.abspath(path)

        # Проверка существования файла
        if not os.path.exists(path):
            raise FileNotExistError(f"Файла '{path}' не существует")
        # Проверка на удаление корневого, родительского и домашнего
        if path == "/" or path == os.path.abspath("/"):
            raise AccessError("Нельзя удалить корневой каталог")
        if (
            path == ".."
            or path == os.path.abspath("..")
            or path == os.path.abspath(os.path.dirname(os.getcwd()))
        ):
            raise AccessError("Нельзя удалить родительский каталог")
        if path == "~" or path == os.path.expanduser("~"):
            raise AccessError("Нельзя удалить домашний каталог")

        # Проверка является ли путь каталогом
        if os.path.isdir(path):
            if not recursion:
                raise TooLittleArgumentsError(
                    f"'{path}' является каталогом, требуется аргумент '-r'"
                )
            check = input(f"Удалить каталог '{path}'? (y/n):").strip().lower()

            if check != "y":
                print("Удаление отменено")
                return

            if not os.access(path, os.W_OK):
                raise AccessError(f"Недостаточно прав для удаления '{path}'")

            shutil.rmtree(path)

        else:
            if recursion:
                raise TooManyArgumentsError("Аргумент -r не требуется")
            os.remove(path)

        logging.info(f"rm {string}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return
