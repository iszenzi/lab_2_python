class CommandError(Exception):
    pass


class FileNotExistError(CommandError):
    pass


class NotIsDirectoryError(CommandError):
    pass


class TooManyArgumentsError(CommandError):
    pass
