import redis
from redis.commands.json import JSON

from sse.backend.environment import get_environments

redis_client = None
redis_json = None


def init_redis():
    global redis_client, redis_json

    env = get_environments()
    connection_pool = redis.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=1,
        socket_timeout=3,
        health_check_interval=60,
    )

    redis_client = redis.Redis(connection_pool=connection_pool)
    redis_json = JSON(redis_client)


def close_redis():
    global redis_client
    redis_client.close()


def save_sse_connection(session_id: str, queue_url: str):
    global redis_json

    prev_sse = redis_json.get("SSE_CONNECTION")

    if prev_sse is None:
        redis_json.set("SSE_CONNECTION", "$", {session_id: queue_url})
    else:
        redis_json.set("SSE_CONNECTION", f"$.{session_id}", queue_url)


def remove_sse_connection(session_id: str):
    global redis_json
    redis_json.delete("SSE_CONNECTION", f"$.{session_id}")
