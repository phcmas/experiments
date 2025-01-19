import asyncio
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from sse.backend.event import EventModel, SSEEvent

logger = logging.getLogger(__name__)
app = FastAPI()
origins = ["http://localhost", "http://localhost:3000", "http://127.0.0.1:3000"]

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


@app.post("/emit")
async def new_event(event: EventModel):
    SSEEvent.add_event(event)
    return {"message": "event added", "count": SSEEvent.count()}


@app.get("/stream")
async def stream(request: Request):
    async def stream_generator():
        while True:
            if await request.is_disconnected():
                logger.info("client disconnected")
                break

            event = SSEEvent.get_event()

            if event:
                yield f"data: {event.model_dump_json()}"

            await asyncio.sleep(1)

    return EventSourceResponse(stream_generator())
