class CommandError(Exception):
    pass


class FileNotExistError(CommandError):
    pass


class NotIsDirectoryError(CommandError):
    pass


class TooManyArgumentsError(CommandError):
    pass


class TooLittleArgumentsError(CommandError):
    pass


class EmptyPathError(CommandError):
    pass


class IsDirectoryError(CommandError):
    pass


class AccessError(CommandError):
    pass


class FileAlreadyExistsError(CommandError):
    pass
