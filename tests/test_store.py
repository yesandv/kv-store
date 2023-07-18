import importlib

from proto import kv_pb2
from utils.str_gen import get_random_str

kv_pb2 = importlib.reload(kv_pb2)


def test_put_data(grpc_server, kv_servicer, stub):
    request = kv_pb2.PutRequest(key=get_random_str(), value=get_random_str())
    response = kv_servicer.PutData(request, stub)
    assert response.success


def test_get_data(grpc_server, kv_servicer, stub):
    key = get_random_str()
    value = get_random_str()
    put_request = kv_pb2.PutRequest(key=key, value=value)
    kv_servicer.PutData(put_request, stub)
    request = kv_pb2.GetRequest(key=key)

    response = kv_servicer.GetData(request, stub)

    assert response.value == value


def test_key_not_found(grpc_server, kv_servicer, stub):
    request = kv_pb2.GetRequest(key="non_existent_key")
    response = kv_servicer.GetData(request, stub)
    assert response.value == "No such key"


def test_client_put_data(grpc_client, mock_stub):
    key = "test_key"
    value = "test_value"
    response = mock_stub.PutData.return_value
    response.success = True

    result = grpc_client.put_data(key, value)

    mock_stub.PutData.assert_called_once()
    assert result


def test_client_get_data(grpc_client, mock_stub):
    key = "yet_another_key"
    value = "yet_another_value"
    response = mock_stub.GetData.return_value
    response.value = value

    result = grpc_client.get_data(key)

    mock_stub.GetData.assert_called_once()
    assert result == value
