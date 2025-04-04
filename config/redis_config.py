import redis

from config.env_config import get_environments, load_environments

load_environments()

connection = None


def create_redis_connection() -> redis.Redis:
    global connection
    env = get_environments()

    connection_pool = redis.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=env.REDIS_MAX_CONNECTION_POOL_SIZE,
        socket_timeout=3,
        health_check_interval=60,
        decode_responses=True,
    )

    connection = redis.Redis(connection_pool=connection_pool)


# redis.Redis
def get_redis_connection():
    global connection
    return connection
