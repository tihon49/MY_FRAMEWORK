import os

from config import MENU
from utils import get_menu_numbers


CHOOSE_FLAG = False


def drow_menu():
    print(MENU)


def get_user_input():
    try:
        user_input = int(input('--> '))
        numbers_list = get_menu_numbers(MENU)
        if user_input in numbers_list:
            return True, user_input
        else:
            message = f'Следует указать одно из: {", ".join(str(i) for i in numbers_list)}'
            print(message)
            return False, message
    except ValueError:
        print('Нужно указать номер меню')
        return False, ''


def main():
    drow_menu()
    while not CHOOSE_FLAG:
        state, choose = get_user_input()
        if state and choose in get_menu_numbers(MENU):
            break
    
    if choose == 1:
        os.chdir('../flask_auto_creator')
        os.system('python3 main.py')
    elif choose == 2:
        os.chdir('../grpc_auto_creator')
        os.system('python3 main.py')


if __name__ == "__main__":
    main()
