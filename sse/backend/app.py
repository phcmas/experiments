import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sse.backend.connection_tracker import close_redis, init_redis
from sse.backend.environment import init_environments
from sse.backend.message_consumer import create_sqs_queue, remove_sqs_queue, start_polling, stop_polling
from sse.backend.router import router

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


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)
