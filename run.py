import os

from config import MENU
from utils import get_menu_numbers, create_flask_app, create_grpc_app



def drow_menu():
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    md = Markdown(MENU)
    console.print(md)


def get_user_input():
    from rich.prompt import IntPrompt
    user_input = IntPrompt.ask(
        '--> ',
        choices=[str(i) for i in get_menu_numbers(MENU)]
    )
    return user_input


def main():
    drow_menu()
    choices_dict = {
        1: create_flask_app,
        2: create_grpc_app
    }
    choose = get_user_input()
    choices_dict.get(choose)()



if __name__ == "__main__":
    main()
