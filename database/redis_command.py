import logging

from config import create_redis_connection, get_redis_connection, init_logging

init_logging()
create_redis_connection()
redis = get_redis_connection()
logger = logging.getLogger(__name__)


def set_command():
    session_id = "20240617081708_pka5f"
    redis.sadd(session_id, 1)
    redis.sadd(session_id, 2)

    result = redis.smembers(session_id)
    result = {int(key) for key in result}

    result = redis.smembers("123123")
    logger.info(result)


def decode_response():
    redis.set("foo", "bar")
    result = redis.get("foo")

    logger.info(result)


if __name__ == "__main__":
    decode_response()
