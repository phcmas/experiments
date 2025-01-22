import asyncio
import logging
import os

import aioboto3
import nanoid

from sse.backend.environment import get_endpoint_url
from sse.backend.event_store import EventModel, push_event

logger = logging.getLogger(__name__)
stop_event = asyncio.Event()
endpoint_url = os.getenv("LOCALSTACK_ENDPOINT_URL")
queue_url = None


def stop_polling():
    if stop_event.is_set():
        return

    stop_event.set()


async def create_sqs_queue():
    global queue_url
    session = aioboto3.Session()
    suffix = nanoid.generate(size=10)

    async with session.client("sqs", endpoint_url=get_endpoint_url()) as sqs:
        response = await sqs.create_queue(
            QueueName=f"events-{suffix}",
            Attributes={"DelaySeconds": "0", "MessageRetentionPeriod": "86400", "VisibilityTimeout": "30"},
        )

        queue_url = response["QueueUrl"]


async def remove_sqs_queue():
    global queue_url
    session = aioboto3.Session()

    async with session.client("sqs", endpoint_url=get_endpoint_url()) as sqs:
        await sqs.delete_queue(QueueUrl=queue_url)


async def start_polling():
    session = aioboto3.Session()

    async with session.client("sqs", endpoint_url=get_endpoint_url()) as sqs:
        while not stop_event.is_set():
            messages = await sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=5)

            for message in messages.get("Messages", []):
                event = EventModel.model_validate_json(message["Body"])
                logger.info(f"received message: {event.model_dump_json()}")

                await push_event(event)
                await sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
