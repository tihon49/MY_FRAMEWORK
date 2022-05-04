Комада для компиляции .proto файла:

python3 -m grpc_tools.protoc -I ./protobufs --python_out=. --grpc_python_out=. ./protobufs/app.proto

