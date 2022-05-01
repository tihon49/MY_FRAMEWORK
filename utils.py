import re


def get_menu_numbers(menu_data: str):
    pattern = re.compile('\d. ')
    result = pattern.findall(menu_data)
    result = [int(i.replace('. ', '')) for i in result]
    return result

