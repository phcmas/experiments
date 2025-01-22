import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

env = None


class Environment(BaseSettings):
    class Config:
        extra = "ignore"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_MAX_CONNECTION_POOL_SIZE: int

    LOCALSTACK_ENDPOINT_URL: str | None = None

    @field_validator("LOCALSTACK_ENDPOINT_URL")
    def validate_localstack_endpoint_url(cls, value: str):
        if os.getenv("PROFILE") == "local" and value is None:
            raise ValueError("LOCALSTACK_ENDPOINT_URL environment variable is not set")

        return value


def init_environments():
    global env

    profile = os.getenv("PROFILE")

    if profile is None:
        raise ValueError("PROFILE environment variable is not set")

    root_path = str(Path(__file__).parents[2])
    env = Environment(_env_file=f"{root_path}/.env.{profile}", _env_file_encoding="utf-8")


def get_endpoint_url() -> str:
    global env
    return env.LOCALSTACK_ENDPOINT_URL


def get_environments() -> Environment:
    global env
    return env
