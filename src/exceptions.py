class CommandError(Exception):
    """Базовые ошибки команд"""

    pass


class FileNotExistError(CommandError):
    """Ошибка, когда файл или путь не существует"""

    pass


class NotIsDirectoryError(CommandError):
    """Ошибка, когда ожидается каталог, а не файл"""

    pass


class TooManyArgumentsError(CommandError):
    """Ошибка избыточного количества аргументов функции"""

    pass


class TooLittleArgumentsError(CommandError):
    """Ошибка недостаточного количества аргументов функции"""

    pass


class EmptyPathError(CommandError):
    """Ошибка пустого пути"""

    pass


class IsDirectoryError(CommandError):
    """Ошибка, когда ожидается файл, а не каталог"""

    pass


class AccessError(CommandError):
    """Ошибка недостатка прав доступа"""

    pass


class FileAlreadyExistsError(CommandError):
    """Ошибка, когда файл уже существует"""

    pass


class UnknownFlagError(CommandError):
    """Ошибка неизвестного флага"""

    pass
