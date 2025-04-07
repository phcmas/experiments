import redis

from config.env_config import get_environments, load_environments

connection = None
pubsub_connection = None


def create_redis_connection() -> redis.Redis:
    global connection

    load_environments()
    env = get_environments()

    connection_pool = redis.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=env.REDIS_MAX_CONNECTION_POOL_SIZE,
        health_check_interval=60,
        decode_responses=True,
    )

    connection = redis.Redis(connection_pool=connection_pool)


def create_redis_pubsub_connection() -> redis.asyncio.Redis:
    global pubsub_connection

    load_environments()
    env = get_environments()

    connection_pool = redis.asyncio.ConnectionPool(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        db=0,
        max_connections=env.REDIS_MAX_CONNECTION_POOL_SIZE,
        health_check_interval=60,
    )

    pubsub_connection = redis.asyncio.Redis(connection_pool=connection_pool, decode_responses=True)


# redis.Redis
def get_redis_connection():
    global connection
    return connection


def get_redis_pubsub_connection():
    global pubsub_connection
    return pubsub_connection
