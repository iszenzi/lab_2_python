import os
import logging
import zipfile
import tarfile
from src.exceptions import (
    FileNotExistError,
    NotIsDirectoryError,
    TooManyArgumentsError,
    EmptyPathError,
    TooLittleArgumentsError,
)


def zip(string: str) -> None:
    """
    Создание ZIP-архива из каталога
    :param string: строка аргументов команды zip
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

        folder = parts[0]
        archive = parts[1]

        # Преобразование путей в абсолютные
        folder = os.path.abspath(folder)
        archive = os.path.abspath(archive)

        # Проверка наличия нужного расширения
        if not archive.lower().endswith(".zip"):
            old_name = os.path.splitext(archive)[0]
            archive = old_name + ".zip"

        # Проверка существования файла
        if not os.path.exists(folder):
            raise FileNotExistError(f"Файла {folder} не существует")
        # Проверка является ли путь каталогом
        if not os.path.isdir(folder):
            raise NotIsDirectoryError(f"'{folder}' не является каталогом")

        with zipfile.ZipFile(
            archive, "w", zipfile.ZIP_DEFLATED
        ) as zipka:  # (путь к файлу, режим работы, метод сжатия)
            name = os.path.basename(folder)
            for root, _, files in os.walk(
                folder
            ):  # текущий путь к каталогу, _ - список поддиректорий, список файлов в текущем каталоге
                for file in files:
                    file_path = os.path.join(root, file)  # полный путь к файлу
                    relative_path = os.path.relpath(
                        file_path, folder
                    )  # относительный путь к файлу
                    archive_name = os.path.join(name, relative_path)
                    # Запись файла в архив
                    zipka.write(file_path, archive_name)

        # Логирование успешной команды
        logging.info(f"zip {string}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def unzip(archive: str) -> None:
    """
    Распаковка ZIP-архива в текущий каталог
    :param archive: путь к ZIP-архиву
    """
    try:
        # Проверка ввода пустого пути
        if not archive:
            raise EmptyPathError("Вы не ввели путь к файлу")
        # Проверка количества аргументов
        if len(archive.split()) > 1:
            raise TooManyArgumentsError("Слишком много аргументов")

        archive = archive.strip()

        # Преобразование пути в абсолютный
        archive = os.path.abspath(archive)

        # Проверка наличия нужного расширения
        if not archive.lower().endswith(".zip"):
            raise ValueError("Файл должен иметь расширенение .zip")
        # Проверка существования файла
        if not os.path.exists(archive):
            raise FileNotExistError(f"Файла '{archive}' не существует")
        # Проверка является ли путь каталогом
        if not os.path.isfile(archive):
            raise NotIsDirectoryError(f"'{archive}' не является файлом")

        with zipfile.ZipFile(archive, "r") as zipka:  # (путь к файлу, режим работы)
            # Извелечение всех файлов из архива в текущий каталог
            zipka.extractall()

        # Логирование успешной команды
        logging.info(f"unzip {archive}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def tar(string: str) -> None:
    """
    Создание TAR.GZ-архива из каталога
    :param string: аргументы команды tar
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

        folder = parts[0]
        archive = parts[1]

        # Преобразование путей в абсолютные
        folder = os.path.abspath(folder)
        archive = os.path.abspath(archive)

        # Проверка наличия нужного расширения
        if not archive.lower().endswith(".tar.gz"):
            old_name = os.path.splitext(archive)[0]
            archive = old_name + ".tar.gz"

        if not os.path.exists(folder):
            raise FileNotExistError(f"Файла {folder} не существует")
        # Проверка является ли путь каталогом
        if not os.path.isdir(folder):
            raise NotIsDirectoryError(f"'{folder}' не является каталогом")

        with tarfile.open(archive, "w:gz") as tar:  # (путь к файлу, режим работы)
            # Добваление каталога в архив
            tar.add(folder, arcname=os.path.basename(folder))

        # Логирование успешной команды
        logging.info(f"tar {string}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return


def untar(archive: str) -> None:
    """
    Распаковка TAR.GZ-архива в текущий каталог
    :param archive: путь к TAR.GZ-архиву
    """
    try:
        # Проверка ввода пустого пути
        if not archive:
            raise EmptyPathError("Вы не ввели путь к файлу")
        # Проверка количества аргументов
        if len(archive.split()) > 1:
            raise TooManyArgumentsError("Слишком много аргументов")

        archive = archive.strip()

        # Преобразование пути в абсолютный
        archive = os.path.abspath(archive)

        # Проверка наличия нужного расширения
        if not archive.lower().endswith(".tar.gz"):
            raise ValueError("Файл должен иметь расширенение .tar.gz")
        # Проверка существования файла
        if not os.path.exists(archive):
            raise FileNotExistError(f"Файла '{archive}' не существует")
        # Проверка является ли путь каталогом
        if not os.path.isfile(archive):
            raise NotIsDirectoryError(f"'{archive}' не является файлом")

        with tarfile.open(archive, "r:gz") as tar:  # (путь к файлу, режим работы)
            # Извелечение всех файлов из архива в текущий каталог
            tar.extractall()
        # Логирование успешной команды
        logging.info(f"untar {archive}")
        return

    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"ERROR: {str(e)}")
        return
