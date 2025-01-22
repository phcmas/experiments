import json
import redis
from sse.backend.environment import get_environments


connection = None


def create_redis_connection():
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


def close_redis_connection():
    global connection
    connection.close()


def save_connection_state(session_id: str, queue_url: str):
    global connection

    prev_state = connection.get("SSE_CONNECTION")
    cur_state = json.loads(prev_state) if prev_state else {}
    cur_state[session_id] = queue_url

    connection.set("SSE_CONNECTION", json.dumps(cur_state))


def get_connection_state(session_id: str):
    global connection

    cur_state = connection.get("SSE_CONNECTION")
    return json.loads(cur_state).get(session_id) if cur_state else None
