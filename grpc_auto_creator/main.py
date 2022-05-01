import os
import pathlib

from config import SERVER_DATA, APP_PROTO, MAIN_PY, CLIENT_DATA, REQUIREMENTS_TXT


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


def create_proto():
    create_folder('protobufs')
    os.chdir('protobufs')
    create_file('__init__.py')
    create_file_with_data('app.proto', APP_PROTO)
    os.chdir('../')
    os.system('python3 -m grpc_tools.protoc -I ./protobufs --python_out=. --grpc_python_out=. ./protobufs/app.proto')


def create_grpc_server():
    create_folder('GRPC_APP/server')
    os.chdir('GRPC_APP/server')

    create_file_with_data('requirements.txt', REQUIREMENTS_TXT)
    create_file_with_data('server.py', SERVER_DATA)
    create_proto()


def create_grpc_client():
    create_folder('GRPC_APP/client/app')
    os.chdir('GRPC_APP/client/app')

    create_file_with_data('requirements.txt', REQUIREMENTS_TXT)
    create_file_with_data('main.py', MAIN_PY)

    create_folder('client')
    os.chdir('client')

    create_proto()
    
    create_file_with_data('client.py', CLIENT_DATA)
    print('Для исправления ошибки импорта следует изменить файл '
          'GRPC_APP/client/app/client/app_pb2_grpc.py изменив:\n'
          '"import app_pb2 as app__pb2" на "from . import app_pb2 as app__pb2"\n')


def main():
    CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
    create_grpc_server()
    os.chdir(CURRENT_PATH)
    create_grpc_client()


if __name__ == '__main__':
    main()
