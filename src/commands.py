import os
import logging
from datetime import datetime

from src.exceptions import FileNotExistError, NotIsDirectoryError, TooManyArgumentsError


def ls(string: str):
    """
    Отображает содержимое каталога
    :param string: строка аргументов команды ls
    """
    try:
        # Разбиение строки аргументов на отдельные аргументы
        parts = string.split()
        # Флаг расширенного вывода команды
        long_format = False
        paths = []
        # Флаг успешного выполнения команды
        success_command = True

        for part in parts:
            if part == "-l":
                long_format = True
            else:
                paths.append(part)

        if not parts:
            paths = ["."]
        # Обработка каждого пути из списка аргументов
        for path in paths:
            try:
                if path == "-l" or path.strip() == "-l":
                    path = "."
                    long_format = True

                elif path == ".":
                    path = os.getcwd()

                elif path == "..":
                    path = os.path.dirname(os.getcwd())

                elif path == "~":
                    path = os.path.expanduser("~")
                # Преобразование пути в абсолютный
                path = os.path.abspath(path)
                # Проверка на существование файла
                if not os.path.exists(path):
                    raise FileNotExistError(f"Файла '{path}' не существует")
                # Проверка является ли путь каталогом
                if not os.path.isdir(path):
                    raise NotIsDirectoryError(f"'{path}' не является каталогом")
                # Список файлов в каталоге
                files = os.listdir(path)

                print(f"\n{path}:\n")

                if long_format:
                    for file in files:
                        # Полный путь к файлу
                        file_path = os.path.join(path, file)
                        # Размер файла
                        size = os.path.getsize(file_path)
                        # Дата последнего изменения файла
                        time_change_in_second = os.stat(file_path).st_mtime
                        time_change = datetime.fromtimestamp(
                            time_change_in_second
                        ).strftime("%d-%m-%y %H:%M:%S")
                        if os.path.isdir(file_path):
                            print(
                                f"DIR {file}  SIZE({size}) lAST CHANGE({time_change})"
                            )
                        elif os.path.isfile(file_path):
                            print(
                                f"FILE {file} SIZE({size}) LAST CHANGE({time_change})"
                            )

                elif not long_format:
                    for file in files:
                        # Полный путь к файлу
                        file_path = os.path.join(path, file)
                        if os.path.isdir(file_path):
                            print(f"DIR {file}")
                        elif os.path.isfile(file_path):
                            print(f"FILE {file}")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"ERROR: {str(e)}")
                print(f"\nERROR: {str(e)}\n")
                success_command = False
                continue
        # Логирование успешной команды
        if success_command:
            logging.info(f"ls {string}")

        return
    except Exception as e:
        # Логирование ошибки
        logging.error(f"ERROR: {str(e)}")
        print(f"\nERROR: {str(e)}\n")
        return


def cd(path: str):
    """
    Переход в указанный каталог
    :param path: путь к каталогу
    """
    try:
        # Проверка на количество аргументов команды
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
        # Проверка на существование файла
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
        print(f"\nERROR: {str(e)}\n")
        return
