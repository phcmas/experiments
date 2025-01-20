import asyncio
import logging
import os

import aioboto3

from sse.backend.event import EventModel, push_event

logger = logging.getLogger(__name__)
queue_url = os.getenv("QUEUE_URL")
endpoint_url = os.getenv("LOCALSTACK_ENDPOINT_URL")
stop_event = asyncio.Event()


def stop_polling():
    if stop_event.is_set():
        return

    stop_event.set()


async def polling():
    session = aioboto3.Session()

    async with session.client("sqs", endpoint_url=endpoint_url) as sqs:
        while not stop_event.is_set():
            messages = await sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=5)

            for message in messages.get("Messages", []):
                event = EventModel.model_validate_json(message["Body"])
                logger.info(f"received message: {event.model_dump_json()}")

                await push_event(event)
                await sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
