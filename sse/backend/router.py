import asyncio
import logging

from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

from sse.backend.event import create_event_queue, remove_event_queue
from sse.backend.message_adapter import polling, stop_polling

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


async def lifespan(app: FastAPI):
    """read more about it in the fastapi docs for lifespan (https://fastapi.tiangolo.com/advanced/events/)"""

    asyncio.create_task(polling())
    yield
    stop_polling()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    return {"message": "hello world"}


@app.get("/stream/{session_id}")
async def stream(session_id: str):
    queue = asyncio.Queue()
    create_event_queue(session_id, queue)

    logger.info(f"client connected: {session_id}")

    async def event_generator():
        try:
            while True:
                event = await queue.get()
                yield f"data: {event.model_dump_json()}"
        except asyncio.CancelledError:
            logger.info(f"client disconnected: {session_id}")
            remove_event_queue(session_id)

    return EventSourceResponse(event_generator())
