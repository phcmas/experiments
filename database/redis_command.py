from config import load_environments, logger

# noqa
from redis import Redis  # type: ignore

settings = load_environments()
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def main():
    session_id = "20240617081708_pka5f"
    redis.sadd(session_id, 1)
    redis.sadd(session_id, 2)

    result = redis.smembers(session_id)
    result = {int(key) for key in result}

    result = redis.smembers("123123")
    logger.info(result)


main()
