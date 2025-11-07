import os
import logging
from src.logger import setup_logging
from src.commands import cd, cat, cp, mv
from src.get_ls import ls
from src.get_zip import zip, unzip, tar, untar
from src.get_grep import grep
from src.get_rm import rm


def main():
    while True:
        current_dir = os.getcwd()
        user_input = input(f"{current_dir}$ ")
        if not user_input.strip():
            continue
        args = user_input.split()
        command = args[0]
        argument = " ".join(args[1:])
        if command == "ls":
            ls(argument)
        elif command == "cd":
            cd(argument)
        elif command == "cat":
            cat(argument)
        elif command == "cp":
            cp(argument)
        elif command == "mv":
            mv(argument)
        elif command == "rm":
            rm(argument)
        elif command == "zip":
            zip(argument)
        elif command == "unzip":
            unzip(argument)
        elif command == "tar":
            tar(argument)
        elif command == "untar":
            untar(argument)
        elif command == "grep":
            grep(argument)
        elif command == "exit":
            break
        else:
            e = f"Неизвестная команда '{command}'"
            logging.error(f"ERROR: {e}")
            print(f"ERROR: {e}")
            continue


if __name__ == "__main__":
    setup_logging()
    main()
"""сделать тесты из комбинации команд"""
