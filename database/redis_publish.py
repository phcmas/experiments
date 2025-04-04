import json
import logging

from redis.exceptions import RedisError

from config import create_redis_connection, get_redis_connection, init_logging

init_logging()
create_redis_connection()
redis = get_redis_connection()
logger = logging.getLogger(__name__)


def publish_message(channel: str, message: dict):
    try:
        redis.publish(channel, json.dumps(message))
        logger.info(f"published message: {message} to channel: {channel}")
    except RedisError as e:
        logger.error(f"failed to publish message: {e}")


if __name__ == "__main__":
    message = {"session_id": "20250404042603_moxje", "requested_at": "2023-10-01T12:00:00Z"}
    publish_message("test_channel", message)
