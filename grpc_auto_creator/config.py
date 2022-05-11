REQUIREMENTS_TXT = """grpcio==1.40.0
grpcio-tools==1.40.0
protobuf==3.18.0
six==1.16.0"""


SERVER_DATA = """import os
import asyncio
import logging
import json
import grpc

import app_pb2
import app_pb2_grpc



def get_pwd():
    pwd = os.popen('uname -a').read()
    return pwd


class Server(app_pb2_grpc.GRPCServiceServicer):

    def Test(
            self, request: app_pb2.Request,
            context: grpc.aio.ServicerContext) -> app_pb2.Response:
        '''
        тестовая функция
        '''

        response = {
            'status': 'failed',
            'error': '',
        }

        response.update({
            'data': 'test data',
            'status': 'success'
        })

        return app_pb2.Response(data=json.dumps(response))


async def serve() -> None:
    server = grpc.aio.server()
    app_pb2_grpc.add_GRPCServiceServicer_to_server(Server(), server)
    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)


if __name__ == '__main__':
    asyncio.run(serve())
"""

APP_PROTO = """syntax = "proto3";


message Request {}

message DataRequest {
  string data = 1;
}

message Response {
  string data = 1;
}


service GRPCService {
  rpc Test (Request) returns (Response) {}
}
"""

MAIN_PY = """import json

from client import client


SERVER_IP = 'localhost'
SERVER_PORT = '50052'


with client.ClusterInfo(SERVER_IP, SERVER_PORT) as cunnection:
    data = json.loads(cunnection.test())

print(data)
print('--------------------------------')
print('Статус', data['status'])
print('data', data['data'])
"""

CLIENT_DATA = """import grpc

from . import app_pb2
from . import app_pb2_grpc


class GrpcConnectionError(Exception):
    '''ошибка, вызываемая если сервер недоступен'''

    def __init__(self, message=Exception):
        self.message = message
        print(self.message)

    def __str__(self):
        return str(self.message)


class GrpcClient:
    '''
    Абстракция для grpc client
    '''

    def __init__(self, ip: str, port: str) -> None:
        self.ip = ip
        self.port = port

    @property
    def address(self) -> str:
        return '{}:{}'.format(self.ip, str(self.port))

    def __enter__(self) -> object:
        self.connection = grpc.insecure_channel(self.address)
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()


class ClusterInfo(GrpcClient):
    '''
    создание соединения (context manager) и отправка RPC на сервер
    
    Example:
        with ClusterInfo('192.168.5.155', '50052') as channel:
            node_info = asyncio.run(channel.node_info())
    '''

    def __init__(self, ip: str, port: str, ) -> None:
        super().__init__(ip, port)

    @property
    def stub(self) -> object:
        return app_pb2_grpc.GRPCServiceStub(self.connection)
 
    def test(self):
        '''тестовая функция'''

        try:
            return self.stub.Test(app_pb2.Request()).data
        except Exception as _:
            raise GrpcConnectionError('failed to connect to all addresses')
"""
