import os
import pathlib

from config import (
    INIT_DATA,
    PROJECT_NAME,
    BASE_HTML,
    CONFIG_FILE,
    MODELS_FILE,
    LOGIN_HTML,
    REGISTER_HTML,
    AUTH_PY,
    MAIN_PY,
    INDEX_HTML,
    STYLE_CSS,
)



def create_folder(folder_name, path=None):
    """создать папку с указанным именем"""
    if not path:
        os.system(f'mkdir -p {folder_name}')
    else:
        current_path = pathlib.Path(__file__).parent.resolve()
        os.chdir(path)
        os.system(f'mkdir -p {os.path.join(path, folder_name)}')
        os.chdir(current_path)



def create_file(filename, path=None):
    """создать файл с указаннм именем"""
    if not path:
        os.system(f'touch {filename}')
    else:
        current_path = pathlib.Path(__file__).parent.resolve()
        os.chdir(path)
        os.system(f'touch {filename}')
        os.chdir(current_path)


def create_file_with_data(filename, data, path=None):
    """создать файл с данными"""
    if not path:
        with open(filename, 'w') as f:
            f.write(data)
    else:
        current_path = pathlib.Path(__file__).parent.resolve()
        if not os.path.exists(path):
            os.system(f'mkdir -p {path}')
        os.chdir(path)
        with open(filename, 'w') as f:
            f.write(data)
        os.chdir(current_path)



def main():
    create_folder(PROJECT_NAME)
    os.chdir(PROJECT_NAME)

    create_folder('app')
    os.chdir('app')

    create_folder('views')
    create_folder('static/css')
    create_folder('static/js')
    create_folder('templates')

    create_file_with_data('__init__.py', INIT_DATA)

    create_file_with_data('style.css', STYLE_CSS, 'static/css/')
    create_file('index.js', 'static/js')

    create_file_with_data('base.html', BASE_HTML, 'templates')
    create_file_with_data('index.html', INDEX_HTML, 'templates')
    create_file_with_data('login.html', LOGIN_HTML, 'templates')
    create_file_with_data('register.html', REGISTER_HTML, 'templates')

    create_file_with_data('config.py', CONFIG_FILE)
    create_file_with_data('models.py', MODELS_FILE)
    create_file_with_data('auth.py', AUTH_PY, 'views')
    create_file_with_data('main.py', MAIN_PY, 'views')


if __name__ == '__main__':
    main()


