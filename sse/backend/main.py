import asyncio
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from sse.backend.event import EventModel

logger = logging.getLogger(__name__)
origins = ["http://localhost", "http://localhost:3000", "http://127.0.0.1:3000"]

connections: dict[str, asyncio.Queue] = {}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {"message": "hello world"}


@app.post("/send/{session_id}")
async def send_event(session_id: str, event: EventModel):
    if session_id in connections:
        await connections[session_id].put(event)
        return {"detail": "OK"}
    else:
        raise HTTPException(status_code=404, detail="client not connected")


@app.get("/stream/{session_id}")
async def stream(session_id: str, request: Request):
    queue = asyncio.Queue()
    connections[session_id] = queue

    logger.info(f"client connected: {session_id}")

    async def event_generator():
        try:
            while True:
                event = await queue.get()
                yield f"data: {event.model_dump_json()}"
        except asyncio.CancelledError:
            logger.info(f"client disconnected: {session_id}")
            del connections[session_id]

    return EventSourceResponse(event_generator())

    # return StreamingResponse(event_generator(), media_type="text/event-stream")
