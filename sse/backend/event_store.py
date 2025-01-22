import asyncio
import logging

from fastapi import HTTPException
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class EventModel(BaseModel):
    session_id: str
    inference_seq: int
    sleep_stages: list[int]
    osas: list[int]
    snorings: list[int]


event_store: dict[str, asyncio.Queue] = {}


def remove_event_store(session_id: str):
    global event_store
    if session_id in event_store:
        del event_store[session_id]


def create_event_store(session_id: str):
    global event_store

    if session_id in event_store:
        raise HTTPException(status_code=400, detail="Event store already exists")

    if session_id not in event_store:
        event_store[session_id] = asyncio.Queue()


async def get_event(session_id: str):
    global event_store
    return await event_store[session_id].get()


async def push_event(event: EventModel):
    global event_store

    if event.session_id not in event_store:
        logger.warning(f"Event store not found for session_id: {event.session_id}")
        return

    if event.session_id in event_store:
        await event_store[event.session_id].put(event)
