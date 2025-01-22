import asyncio
import json
import os
from pathlib import Path
from random import random

import aioboto3
import redis
from dotenv import dotenv_values

env = None
connection = None


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
    global connection
    connection_pool = redis.ConnectionPool(host=env["REDIS_HOST"], port=env["REDIS_PORT"], db=0, max_connections=1)
    connection = redis.Redis(connection_pool=connection_pool)


async def send_event(boto3_session, session_id, queue_url):
    message = {
        "session_id": session_id,
        "inference_seq": random.randint(1, 10),
        "sleep_stage": [0, 0, 1, 1, 0, 1, 1, 1, 1],
        "osas": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "snorings": [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    }

    async with boto3_session.client("sqs", endpoint_url=env["LOCALSTACK_ENDPOINT_URL"]) as sqs:
        await sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))


async def send_events():
    cur_sse = connection.get("SSE_CONNECTION")

    if cur_sse is None:
        return

    boto3_session = aioboto3.Session()

    for session_id, queue_url in cur_sse.items():
        await send_event(boto3_session, session_id, queue_url)


async def trigger():
    init_envirnoment()
    init_redis()

    await send_events()


if __name__ == "__main__":
    asyncio.run(trigger())
