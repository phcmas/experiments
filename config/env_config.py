import os
from typing import Optional

from dotenv import dotenv_values
from pydantic_settings import BaseSettings

from config.logging_config import logger

env = None


class Environments(BaseSettings):
    class Config:
        extra = "ignore"

    AWS_REGION: str
    AWS_PROFILE: str
    LOCALSTACK_ENDPOINT_URL: Optional[str] = None
    SQS_INFERENCE_URL: Optional[str]
    UPLOAD_API_BASE_URL: Optional[str]
    MEL_FILE_DIR: Optional[str]
    DATADOG_API_KEY: Optional[str]
    DATADOG_APP_KEY: Optional[str]
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]
    REDIS_MAX_CONNECTION_POOL_SIZE: Optional[int]
    RDS_HOST: Optional[str]
    RDS_PORT: Optional[int]
    RDS_USERNAME: Optional[str]
    RDS_PASSWORD: Optional[str]


def load_environments() -> Environments:
    global env
    if env is not None:
        return

    profile = os.getenv("PROFILE")
    allowed_profiles = ["live", "test", "local"]

    if profile not in allowed_profiles:
        logger.error(f"PROFILE must one of {allowed_profiles}")
        raise

    current_path = os.path.dirname(os.path.abspath(__file__))
    outward_once = os.path.join(current_path, os.pardir)
    dotenv_path = os.path.abspath(outward_once)
    values = dotenv_values(f"{dotenv_path}/.env.{profile}")

    env = Environments(**values)


def get_environments() -> Environments:
    global env
    return env
