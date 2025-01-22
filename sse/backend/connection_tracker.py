import json
import redis
from sse.backend.environment import get_environments
from sse.backend.message_consumer import queue_url


connection = None


async def create_redis_connection():
    global connection

    env = get_environments()

    connection_pool = redis.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=env.REDIS_MAX_CONNECTION_POOL_SIZE,
        socket_timeout=3,
        health_check_interval=60,
    )

    connection = redis.Redis(connection_pool=connection_pool)


async def close_redis_connection():
    global connection
    connection.close()


async def save_connection_state(session_id: str):
    global connection

    prev = json.loads(connection.get("CONNECTION"), {})
    prev[session_id] = queue_url

    connection.set("CONNECTION", json.dumps(prev))


async def get_connection_state(session_id: str):
    global connection

    result = json.loads(connection.get("CONNECTION"), {})
    return result.get(session_id)
