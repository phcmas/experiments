import logging

import msgpack
import msgpack_numpy as m
from redis import Redis

from config.env_config import load_environments
from config.redis_config import create_redis_connection, get_redis_connection

logger = logging.getLogger(__name__)


def restore(bin: bytes):
    return msgpack.unpackb(bin, object_hook=m.decode, strict_map_key=False)


def check_model_prediction(conn: Redis, session_id: str):
    value = conn.get(f"MODEL_PREDICTION:{session_id}")

    if value is not None:
        prediction = restore(value)
        logger.info(f"model prediction for session {session_id}: {prediction.keys()}")


def main():
    load_environments()
    create_redis_connection()

    conn = get_redis_connection()

    session_ids = ["20250105150146_ynunx"]

    for session_id in session_ids:
        check_model_prediction(conn, session_id)


main()
