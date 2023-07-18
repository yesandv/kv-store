# Key-Value Store

A key-value store built with gRPC and Redis in a Docker container.
Covered with some unit and integration tests using pytest.

### Build an image and start containers:
```shell
docker-compose up --build
```

### Run the script inside a kv-app container:
```shell
docker exec -i -t kv-app sh start.sh
```
