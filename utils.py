import re
import os


def get_menu_numbers(menu_data: str) -> list:
    """возвращает номера пунктов мню в виде списка int()"""
    pattern = re.compile('\d. ')
    result = pattern.findall(menu_data)
    result = [int(i.replace('. ', '')) for i in result]
    return result


def create_flask_app():
    """создать flask приложение"""
    os.chdir('flask_auto_creator')
    os.system('python3 main.py')


def create_grpc_app():
    """создать grpc приложение"""
    os.chdir('grpc_auto_creator')
    os.system('python3 main.py')

