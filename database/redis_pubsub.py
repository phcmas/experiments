import asyncio
import json
import logging

from redis.client import PubSub
from redis.exceptions import RedisError

from config import init_logging
from config.redis_config import create_redis_pubsub_connection, get_redis_pubsub_connection

init_logging()
create_redis_pubsub_connection()
redis = get_redis_pubsub_connection()
logger = logging.getLogger(__name__)


async def publish_message(channel, message):
    try:
        await redis.publish(channel, json.dumps(message))
        logger.info(f"published message, {message}")
    except RedisError as e:
        logger.error(f"failed to publish message: {e}")


async def publish_messages(channel):
    for i in range(100):
        await publish_message(channel, {"count": i})
        await asyncio.sleep(3)


async def unsubscribe_from_channel(pubsub: PubSub | None, channel: str):
    if not pubsub:
        return

    try:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
    except RedisError as e:
        logger.warning(f"failed to unsubscribe from channel: {e}")


async def listen_to_channel(channel: str):
    try:
        pubsub = redis.pubsub()
        await pubsub.subscribe(channel)

        logger.info(f"subscribe to channel: {channel}")

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            logger.info(f"received message: {json.loads(message['data'])}")

    except RedisError as e:
        logger.error(f"redis error: {e}")
    except Exception as e:
        logger.error(f"error: {e}")
    finally:
        await unsubscribe_from_channel(pubsub, channel)
        await asyncio.sleep(5)


async def subscribe_to_channel(channel: str):
    while True:
        await listen_to_channel(channel)


if __name__ == "__main__":
    channel = "test_channel"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(subscribe_to_channel(channel))
    loop.create_task(publish_messages(channel))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt: exiting")
    finally:
        loop.close()
