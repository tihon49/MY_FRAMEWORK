import re


def get_menu_numbers(menu_data: str) -> list:
    """возвращает номера пунктов мню в виде списка int()"""
    pattern = re.compile('\d. ')
    result = pattern.findall(menu_data)
    result = [int(i.replace('. ', '')) for i in result]
    return result

