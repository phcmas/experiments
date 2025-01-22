import asyncio
import logging

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from sse.backend.connection_tracker import remove_sse_connection, save_sse_connection
from sse.backend.event_store import create_event_store, get_event, remove_event_store
from sse.backend.message_consumer import get_queue_url

logger = logging.getLogger(__name__)
router = APIRouter(tags=["sse"])


@router.get("/")
async def health():
    return {"message": "hello world"}


@router.get("/v1/stream/{session_id}")
async def stream(session_id: str):
    create_event_store(session_id)
    save_sse_connection(session_id, get_queue_url())

    async def send_event():
        try:
            while True:
                event = await get_event(session_id)
                logger.info(f"sending event: {session_id}")
                yield f"data: {event.model_dump_json()}"
        except asyncio.CancelledError:
            logger.info(f"client disconnected: {session_id}")
            remove_event_store(session_id)
            remove_sse_connection(session_id)

    return EventSourceResponse(send_event())
