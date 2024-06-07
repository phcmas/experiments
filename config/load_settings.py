import os

from dotenv import dotenv_values
from pydantic_settings import BaseSettings

from config.config_logging import logger


class Environments(BaseSettings):
    AWS_REGION: str
    AWS_PROFILE: str
    ENDPOINT_URL: str
    SQS_URL: str
    UPLOAD_API_BASE_URL: str
    MEL_FILE_DIR: str
    AI_MODEL_DIR: str
    DATADOG_API_KEY: str
    DATADOG_APP_KEY: str


def load_settings() -> Environments:
    profile = os.getenv("PROFILE")
    allowed_profiles = ["live", "test", "local"]

    if profile not in allowed_profiles:
        logger.error(f"PROFILE must one of {allowed_profiles}")
        raise

    current_path = os.path.dirname(os.path.abspath(__file__))
    outward_once = os.path.join(current_path, os.pardir)
    dotenv_path = os.path.abspath(outward_once)
    values = dotenv_values(f"{dotenv_path}/.env.{profile}")

    return Environments(**values)
