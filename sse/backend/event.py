import asyncio
from pydantic import BaseModel


class EventModel(BaseModel):
    session_id: str
    sleep_stages: list[int]
    osas: list[int]
    snorings: list[int]


events: dict[str, asyncio.Queue] = {}


def remove_event_queue(session_id: str):
    global events
    if session_id in events:
        del events[session_id]


def create_event_queue(session_id: str):
    global events
    if session_id not in events:
        events[session_id] = asyncio.Queue()


async def get_event(session_id: str):
    global events
    return await events[session_id].get()


async def push_event(event: EventModel):
    global events
    if event.session_id in events:
        await events[event.session_id].put(event)
