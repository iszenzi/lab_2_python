import os
from src.logger import setup_logging
from src.commands import ls, cd, cat, cp, mv


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
        if command == "cd":
            cd(argument)
        if command == "cat":
            cat(argument)
        if command == "exit":
            break
        if command == "cp":
            cp(argument)
        if command == "mv":
            mv(argument)


if __name__ == "__main__":
    setup_logging()
    main()


"""
нужно ли разбираться с правами доступа? в команде cp нужно проверять права доступа? в команде ls выводить права доступа

"""
