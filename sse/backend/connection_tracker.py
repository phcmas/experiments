import json

import redis

from sse.backend.environment import get_environments

connection = None


def init_redis():
    global connection

    env = get_environments()
    connection_pool = redis.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=1,
        socket_timeout=3,
        health_check_interval=60,
    )

    connection = redis.Redis(connection_pool=connection_pool)


def close_redis():
    global connection
    connection.close()


def save_sse_connection(session_id: str, queue_url: str):
    global connection

    prev_sse = connection.get("SSE_CONNECTION")
    cur_sse = json.loads(prev_sse) if prev_sse else {}
    cur_sse[session_id] = queue_url

    connection.set("SSE_CONNECTION", json.dumps(cur_sse))
