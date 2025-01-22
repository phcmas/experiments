import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sse.backend.connection_tracker import close_redis, init_redis
from sse.backend.environment import init_environments
from sse.backend.message_consumer import create_sqs_queue, remove_sqs_queue, start_polling, stop_polling

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


async def lifespan(app: FastAPI):
    """read more about it in the fastapi docs for lifespan (https://fastapi.tiangolo.com/advanced/events/)"""

    init_environments()
    init_redis()
    await create_sqs_queue()
    asyncio.create_task(start_polling())
    yield
    stop_polling()
    await remove_sqs_queue()
    close_redis()


origins = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
