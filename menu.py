import os

from config import MENU
from utils import get_menu_numbers



def drow_menu():
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    md = Markdown(MENU)
    console.print(md)


def get_user_input():
    from rich.prompt import Prompt
    user_input = Prompt.ask(
        '--> ',
        choices=[str(i) for i in get_menu_numbers(MENU)]
    )
    return user_input


def main():
    drow_menu()
    choose = get_user_input()

    if choose == '1':
        os.chdir('flask_auto_creator')
        os.system('python3 main.py')
    elif choose == '2':
        os.chdir('grpc_auto_creator')
        os.system('python3 main.py')


if __name__ == "__main__":
    main()
