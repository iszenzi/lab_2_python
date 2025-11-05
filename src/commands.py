import os
import logging
import shutil

from src.exceptions import (
    FileNotExistError,
    NotIsDirectoryError,
    TooManyArgumentsError,
    EmptyPathError,
    IsDirectoryError,
    TooLittleArgumentsError,
    AccessError,
    FileAlreadyExistsError,
)


def cd(path: str) -> None:
    """
    Переход в указанный каталог
    :param path: путь к каталогу
    """
    try:
        # Проверка количество аргументов команды
        if len(path.split()) > 1:
            raise TooManyArgumentsError("Слишком много аргументов")

        path = path.strip()

        if path == "":
            path = "."

        if path == ".":
            logging.info("cd .")
            return

        elif path == "..":
            path = os.path.dirname(os.getcwd())

        elif path == "~":
            path = os.path.expanduser("~")
        # Преобразование пути в абсолютный
        path = os.path.abspath(path)
        # Проверка существования файла
        if not os.path.exists(path):
            raise FileNotExistError(f"Файла '{path}' не существует")
        # Проверка является ли путь каталогом
        if not os.path.isdir(path):
            raise NotIsDirectoryError(f"'{path}' не является каталогом")
        # Изменение каталога
        os.chdir(path)
        # Логирование успешной команды
        logging.info(f"cd {path}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def cat(path: str) -> None:
    """
    Вывод содержимого указанного файла
    :param path: путь к файлу
    """
    try:
        # Проверка ввода пустого пути
        if not path:
            raise EmptyPathError("Вы не ввели путь к файлу")
        # Проверка количества аргументов
        if len(path.split()) > 1:
            raise TooManyArgumentsError("Слишком много аргументов")

        path = path.strip()
        # Преобразование пути в абсолютный
        path = os.path.abspath(path)
        # Проверка существования файла
        if not os.path.exists(path):
            raise FileNotExistError(f"Файла '{path}' не существует")
        # Проверка является ли путь каталогом
        if os.path.isdir(path):
            raise IsDirectoryError(f"'{path}' является каталогом")

        file = open(path)
        for line in file.readlines():
            print(line, end="")
        # Логирование успешной команды
        logging.info(f"cat {path}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def cp(string: str) -> None:
    """
    Копирование файла или каталога в указанный каталог
    :param string: строка аргументов команды cp
    """
    try:
        # Проверка ввода пустого пути
        if not string:
            raise EmptyPathError("Вы не ввели путь к файлу")

        parts = string.split()
        # Проверка количества аргументов
        if len(parts) < 2:
            raise TooLittleArgumentsError("Слишком мало аргументов")
        # Флаг рекурсивного копирования
        recursion = False
        # Источник
        source = None
        # Путь назначения
        destination = None

        for part in parts:
            if part == "-r":
                recursion = True
            elif source is None:
                source = part
            elif destination is None:
                destination = part
            else:
                raise TooManyArgumentsError("Cлишком много аргументов")

        if source is None or destination is None:
            raise ValueError("Источник или путь назначения отсутствуют")
        # Преобразование путей в абсолютный
        source = os.path.abspath(source)
        destination = os.path.abspath(destination)
        # Проверка существования файла
        if not os.path.exists(source):
            raise FileNotExistError(f"Файла '{source}' не существует")
        if not os.path.exists(destination):
            raise FileNotExistError(f"Файла '{destination}' не существует")
        # Проверка является ли путь каталогом
        if not os.path.isdir(destination):
            raise NotIsDirectoryError(f"'{destination}' не является каталогом'")
        # Проверка является ли источник каталогом
        if os.path.isdir(source):
            # Проверка наличия аргумента '-r'
            if not recursion:
                raise TooLittleArgumentsError(
                    f"'{source}' является каталогом, требуется аргумент '-r'"
                )
            shutil.copytree(source, destination, dirs_exist_ok=True)
            # Логирование успешной команды
            logging.info(f"cp {string}")
            return
        else:
            # Проверка отсутствия аргумента '-r'
            if recursion:
                raise TooManyArgumentsError("Аргумент '-r' не требуется")
            shutil.copy2(source, destination)
            # Логирование успешной команды
            logging.info(f"cp {string}")
            return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def mv(string: str) -> None:
    """
    Перемещение или переименование файла/каталога
    :param string: строка аргументов команды mv
    """
    try:
        # Проверка ввода пустого пути
        if not string:
            raise EmptyPathError("Вы не ввели путь к файлу")

        parts = string.split()
        # Проверка количества аргументов
        if len(parts) > 2:
            raise TooManyArgumentsError("Слишком много аргументов")
        if len(parts) < 2:
            raise TooLittleArgumentsError("Слишком мало аргументов")
        # Источник
        source = parts[0]
        # Путь назначения
        destination = parts[1]

        # Преобразование путей в абсолютный
        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        # Проверка существования файла
        if not os.path.exists(source):
            raise FileNotExistError(f"Файла '{source}' не существует")
        # Проверка права чтения файла
        if not os.access(source, os.R_OK):
            raise AccessError(f"Нет прав на чтение '{source}'")
        # Родительская папка каталога назначения
        destination_dirname = os.path.dirname(destination)
        # Проверка существования родительской папки каталога назначения
        if not os.path.exists(destination_dirname):
            raise FileExistsError(f"Каталога '{destination_dirname}' не существует")
        # Проверка права записи в каталог
        if not os.access(destination_dirname, os.W_OK):
            raise AccessError(f"Нет прав на запись в каталог '{destination_dirname}'")

        # Существует ли путь назначения и является ли он каталогом
        if os.path.exists(destination) and os.path.isdir(destination):
            destination = os.path.join(destination, os.path.basename(source))
            # Есть ли в папке уже такой файл
            if os.path.exists(destination):
                raise FileAlreadyExistsError(f"'{destination}' уже существует")
            shutil.move(source, destination)
            logging.info(f"mv {string}")
            return
        # Если каталог назначения существует и он файл
        elif os.path.exists(destination) and os.path.isfile(destination):
            raise FileAlreadyExistsError(f"'{destination}' уже существует")

        shutil.move(source, destination)
        logging.info(f"mv {string}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


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
        for part in parts:
            if part == "-r":
                recursion = True
            elif path is None:
                path = part
            else:
                raise TooManyArgumentsError("Cлишком много аргументов")
        if path is None:
            raise EmptyPathError("Вы не ввели путь к файлу")
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
            logging.info(f"rm {string}")
            return
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
