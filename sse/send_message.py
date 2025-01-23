import asyncio
import json
import logging
import os
import random
import sys
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
    profile = os.getenv("PROFILE") or "local"
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


async def send_event(boto3_session, session_id: str, queue_url: str, messages: list[dict]):
    async with boto3_session.client("sqs", endpoint_url=env["LOCALSTACK_ENDPOINT_URL"]) as sqs:
        for message in messages:
            await sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
            logger.info(f"sent message, session_id: {session_id}")


async def unicast(session_id: str, message_count: int):
    cur_sse = redis_json.get("SSE_CONNECTION", f"$.{session_id}")
    boto3_session = aioboto3.Session()

    if len(cur_sse) == 0:
        logger.error(f"session_id: {session_id} is not found")
        return

    messages = [create_random_message(session_id) for _ in range(message_count)]
    await send_event(boto3_session, session_id, cur_sse[0], messages)


async def broadcast():
    cur_sses = redis_json.get("SSE_CONNECTION", "$")
    boto3_session = aioboto3.Session()

    for cur_sse in cur_sses:
        for session_id, queue_url in cur_sse.items():
            messages = [create_random_message(session_id) for _ in range(3)]
            await send_event(boto3_session, session_id, queue_url, messages)


async def send_message():
    init_envirnoment()
    init_redis()

    if len(sys.argv) > 2:
        session_id, message_count = sys.argv[1], int(sys.argv[2])
        await unicast(session_id, message_count)
    else:
        await broadcast()


if __name__ == "__main__":
    asyncio.run(send_message())
