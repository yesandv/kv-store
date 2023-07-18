from concurrent import futures
from unittest import mock

import grpc
import pytest

from client import Client
from proto import kv_pb2_grpc
from server import KeyValueStore
from utils.config import store_settings


@pytest.fixture
def kv_servicer():
    return KeyValueStore(store_settings.host, store_settings.test_redis_port)


@pytest.fixture
def grpc_server(kv_servicer):
    server = grpc.server(futures.ThreadPoolExecutor())
    kv_pb2_grpc.add_KeyValueStoreServicer_to_server(kv_servicer, server)
    server.add_insecure_port(
        f"{store_settings.host}:{store_settings.grpc_port}"
    )
    server.start()
    yield server
    server.stop(0)


@pytest.fixture
def stub():
    channel = grpc.insecure_channel(
        f"{store_settings.host}:{store_settings.grpc_port}"
    )
    stub = kv_pb2_grpc.KeyValueStoreStub(channel)
    return stub


@pytest.fixture
def grpc_client():
    return Client()


@pytest.fixture
def mock_stub(grpc_client):
    grpc_client.stub = mock.Mock()
    return grpc_client.stub
