import logging
import time

from redis.exceptions import RedisError
from redis.client import PubSub

from config import create_redis_connection, get_redis_connection, init_logging

init_logging()
create_redis_connection()
redis = get_redis_connection()
logger = logging.getLogger(__name__)


def unsubscribe_from_channel(pubsub: PubSub | None, channel: str):
    if not pubsub:
        return

    try:
        pubsub.unsubscribe(channel)
        pubsub.close()
    except Exception as e:
        logger.warning(f"failed to unsubscribe from channel: {e}")


def listen_to_channel(channel: str):
    try:
        pubsub = redis.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message["type"] != "message":
                continue

            logger.info(f"received message: {message['data'].decode('utf-8')}")

    except RedisError as e:
        logger.error(f"redis error: {e}")
    except Exception as e:
        logger.error(f"error: {e}")
    finally:
        unsubscribe_from_channel(pubsub, channel)
        time.sleep(1)


def subscribe_to_channel(channel):
    logger.info(f"subscribe to channel: {channel}")

    while True:
        listen_to_channel(channel)


if __name__ == "__main__":
    subscribe_to_channel("test_channel")
