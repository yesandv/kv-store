import importlib
import signal
from concurrent import futures

import grpc
import redis

from proto import kv_pb2_grpc, kv_pb2
from utils.config import store_settings
from utils.logging_config import logger


kv_pb2 = importlib.reload(kv_pb2)


class KeyValueStore(kv_pb2_grpc.KeyValueStoreServicer):

    def __init__(
            self,
            redis_host: str = store_settings.redis_host,
            redis_port: int = store_settings.redis_port,
    ):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def GetData(self, request, context) -> str:
        value = self.redis_client.get(request.key)
        if value:
            return kv_pb2.GetResponse(value=value.decode("utf-8"))
        else:
            logger.info("Request key '%s' is not found", request.key)
            return kv_pb2.GetResponse(value="No such key")

    def PutData(self, request, context) -> bool:
        success = self.redis_client.set(
            request.key, request.value.encode("utf-8")
        )
        return kv_pb2.PutResponse(success=success)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    kv_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStore(), server)
    server.add_insecure_port(
        f"{store_settings.host}:{store_settings.grpc_port}"
    )
    server.start()
    logger.info(
        "Server is started at %s:%s",
        store_settings.host,
        store_settings.grpc_port,
    )
    try:
        signal.signal(signal.SIGINT, lambda sig, frame: server.stop(0))
        signal.signal(signal.SIGTERM, lambda sig, frame: server.stop(0))
        server.wait_for_termination()
        logger.info("Terminating a session")
    except (KeyboardInterrupt, InterruptedError):
        server.stop(0)
        logger.info("Server is stopped")


if __name__ == "__main__":
    serve()
