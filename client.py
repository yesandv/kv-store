import importlib

import grpc

from proto import kv_pb2
from proto import kv_pb2_grpc as kv_pb2_grpc
from utils.config import store_settings
from utils.logging_config import logger

kv_pb2 = importlib.reload(kv_pb2)


class Client:

    def __init__(self):
        self.channel = grpc.insecure_channel(
            f"{store_settings.host}:{store_settings.grpc_port}"
        )
        self.stub = kv_pb2_grpc.KeyValueStoreStub(self.channel)

    def put_data(self, key: str, value: str) -> bool:
        request = kv_pb2.PutRequest(key=key, value=value)
        response = self.stub.PutData(request)
        return response.success

    def get_data(self, key: str) -> str:
        request = kv_pb2.GetRequest(key=key)
        response = self.stub.GetData(request)
        return response.value

    def run(self):
        while True:
            try:
                key, *value = input("Waiting for input:\n").split(maxsplit=1)
                if value:
                    response = self.put_data(key=key, value=value[0])
                    logger.info(
                        "Stored successfully"
                        if response
                        else "Fail to store data"
                    )
                else:
                    response = self.get_data(key=key)
                    print(response)
            except KeyboardInterrupt:
                break


def main():
    try:
        Client().run()
    except grpc.RpcError:
        logger.exception("Server is not running")


if __name__ == "__main__":
    main()
