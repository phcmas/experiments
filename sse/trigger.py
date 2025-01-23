import asyncio
import json
import logging
import os
import random
from pathlib import Path

import aioboto3
import redis
from dotenv import dotenv_values
from redis.commands.json import JSON

env = None
redis_client = None
redis_json = None


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_envirnoment():
    global env
    profile = os.getenv("PROFILE")

    if profile is None:
        raise ValueError("PROFILE is not set")

    file_path = f"{str(Path(__file__).parents[1])}/.env.{profile}"
    env = dict(dotenv_values(file_path))

    if profile == "local" and env["LOCALSTACK_ENDPOINT_URL"] is None:
        raise ValueError("LOCALSTACK_ENDPOINT_URL is not set")


def init_redis():
    global redis_client, redis_json
    connection_pool = redis.ConnectionPool(host=env["REDIS_HOST"], port=env["REDIS_PORT"], db=0, max_connections=1)
    redis_client = redis.Redis(connection_pool=connection_pool)
    redis_json = JSON(redis_client)


def create_random_message(session_id: str):
    return {
        "session_id": session_id,
        "inference_seq": random.randint(0, 10),
        "sleep_stages": [random.randint(0, 2) for _ in range(10)],
        "osas": [random.randint(0, 1) for _ in range(10)],
        "snorings": [random.randint(0, 1) for _ in range(10)],
    }


async def send_event(boto3_session, session_id, queue_url):
    messages = [create_random_message(session_id) for _ in range(random.randint(1, 3))]

    async with boto3_session.client("sqs", endpoint_url=env["LOCALSTACK_ENDPOINT_URL"]) as sqs:
        for message in messages:
            await sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
            logger.info(f"sent message, session_id: {session_id}")


async def send_events():
    cur_sse = redis_json.get("SSE_CONNECTION", "$")
    boto3_session = aioboto3.Session()

    for session_id, queue_url in cur_sse[0].items():
        await send_event(boto3_session, session_id, queue_url)


async def trigger():
    init_envirnoment()
    init_redis()

    await send_events()


if __name__ == "__main__":
    asyncio.run(trigger())
