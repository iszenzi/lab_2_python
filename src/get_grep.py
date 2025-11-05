import os
import re
import logging
from src.exceptions import (
    EmptyPathError,
    TooLittleArgumentsError,
    TooManyArgumentsError,
    UnknownFlagError,
    FileNotExistError,
    NotIsDirectoryError,
)


def grep(string: str) -> None:
    """
    Поиск строк, соответсвующих шаблону в файлах
    :param string: строка аргументов команды grep
    """
    try:
        # Проверка ввода пустого пути
        if not string:
            raise EmptyPathError("Вы не ввели паттерн и путь")

        parts = string.split()

        # Проверка количества аргументов
        if len(parts) < 2:
            raise TooLittleArgumentsError("Слишком мало аргументов")

        # Флаг рекурсивного поиска
        recursion = False
        # Флаг игнорирования регистра
        ignore_register = False
        pattern = None
        path = None

        # Обработка аргументов
        for part in parts:
            if part == "-r":
                recursion = True
            elif part == "-i":
                ignore_register = True
            elif pattern is None:
                pattern = part
            elif path is None:
                path = part
            else:
                if part.startswith("-"):
                    raise UnknownFlagError(f"Неизвестный флаг '{part}'")
                else:
                    raise TooManyArgumentsError("Слишком много аргументов")

        if pattern is None or path is None:
            raise ValueError("Паттерн или путь не указаны")

        # Компилирование регулярного выражения
        if ignore_register:
            flags = re.IGNORECASE
        else:
            flags = re.RegexFlag(0)
        regex = re.compile(pattern, flags)

        # Преобразование пути в абсолютный
        path = os.path.abspath(path)

        # Проверка существования пути
        if not os.path.exists(path):
            raise FileNotExistError(f"Пути '{path}' не существует")

        # Если путь файл
        if os.path.isfile(path):
            for line_number, line in enumerate(open(path, "r", encoding="utf-8"), 1):
                if regex.search(line):
                    print(f"{path}: Строка № {line_number}: {line}")

        # Если путь каталог
        elif os.path.isdir(path):
            # Если есть флага на рекурсивный поиск
            if recursion:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            try:
                                for line_number, line in enumerate(
                                    open(file_path, "r", encoding="utf-8"), 1
                                ):
                                    if regex.search(line):
                                        print(
                                            f"{file_path}: Строка № {line_number}: {line.strip()}"
                                        )
                            except Exception as e:
                                logging.error(f"ERROR: {file_path}: {str(e)}")
                                print(f"ERROR: {file_path}: {str(e)}")

            # Если нет флага на рекурсивный поиск
            else:
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if os.path.isfile(file_path):
                        try:
                            for line_number, line in enumerate(
                                open(file_path, "r", encoding="utf-8"), 1
                            ):
                                if regex.search(line):
                                    print(
                                        f"{file_path}: Строка № {line_number}: {line.strip()}"
                                    )
                        except Exception as e:
                            logging.error(f"ERROR: {file_path}: {str(e)}")
                            print(f"ERROR: {file_path}: {str(e)}")
        else:
            raise NotIsDirectoryError(f"'{path}' не является файлом или каталогом")

        # Логирование успешной команды
        logging.info(f"grep {string}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return
