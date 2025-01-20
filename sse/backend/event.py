import asyncio
from pydantic import BaseModel

events: dict[str, asyncio.Queue] = {}


class EventModel(BaseModel):
    session_id: str
    sleep_stages: list[int]
    osas: list[int]
    snorings: list[int]


def remove_event_queue(session_id: str):
    global events
    if session_id in events:
        del events[session_id]


def create_event_queue(session_id: str, queue: asyncio.Queue):
    global events
    events[session_id] = queue


async def push_event(event: EventModel):
    global events
    if event.session_id in events:
        await events[event.session_id].put(event)
