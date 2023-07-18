from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    title: str = "Key-Value Store"
    host: str = "localhost"
    grpc_port: str = "50051"
    redis_host: str = "redis"
    redis_port: int = 6379
    test_redis_port: int = 6380

    class Config:
        env_file = "../.env"


store_settings = Settings()
