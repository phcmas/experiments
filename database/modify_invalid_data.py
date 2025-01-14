import json
import logging

import pymysql
import requests
from pymysql.cursors import DictCursor
from redis import Redis

from config.env_config import load_environments
from config.rds_config import create_rds_connections, get_rds_connections
from config.redis_config import create_redis_connection, get_redis_connection

logger = logging.getLogger(__name__)


def fetch_sessions_with_invalid_data(rds_conn: pymysql.connect) -> list[str]:
    try:
        query = """
        SELECT ss.session_id, ss.end_time, ss.unexpected_end_time, ss.api_key, ss.user_id
          FROM sleep_session ss
         INNER JOIN model_prediction mp on ss.session_id = mp.session_id
         WHERE mp.start_mel_seq = 0
           AND mp.end_mel_seq < 79
           AND ss.state = "COMPLETE"
           AND ss.complete_time < "2025-01-14 06:00:00"
           AND ss.model_name = "highball"
        """

        with rds_conn.cursor(DictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            {
                "session_id": row["session_id"],
                "end_time": row["end_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "unexpected_end_time": row["unexpected_end_time"].strftime("%Y-%m-%dT%H:%M:%SZ")
                if row["unexpected_end_time"]
                else None,
                "api_key": row["api_key"],
                "user_id": row["user_id"],
            }
            for row in rows
        ]

    except pymysql.MySQLError as e:
        logger.error("fails to fetch sessions with invalid data", exc_info=e)
        raise e


def remove_session_in_cache(redis_conn: Redis, session_id: str):
    try:
        redis_conn.delete(f"SLEEP_SESSION:{session_id}")

    except Exception as e:
        logger.error("fails to remove session in cache", exc_info=e)
        raise e


def remove_pp_and_stats(rds_conn: pymysql.connect, session_id: str):
    tables = ["post_processing_result", "osa_post_processing_result", "snoring_post_processing_result", "sleep_stat"]

    try:
        with rds_conn.cursor() as cursor:
            for table in tables:
                query = f"DELETE FROM {table} WHERE session_id = '{session_id}';"
                cursor.execute(query)

            rds_conn.commit()

    except pymysql.MySQLError as e:
        logger.error("fails to remove post processing and statistics", exc_info=e)
        raise e


def update_to_open(rds_conn: pymysql.connect, session_id: str):
    try:
        query = f"UPDATE sleep_session ss SET state = 'OPEN' WHERE session_id = '{session_id}';"

        with rds_conn.cursor() as cursor:
            cursor.execute(query)
            rds_conn.commit()

    except pymysql.MySQLError as e:
        logger.error("fails to update session state to OPEN", exc_info=e)
        raise e


def update_time(rds_conn: pymysql.connect, session_id: str, end_time: str, unexpected_end_time: str | None = None):
    try:
        query = (
            f"UPDATE sleep_session ss SET end_time = '{end_time}', unexpected_end_time = '{unexpected_end_time}' WHERE session_id = '{session_id}';"
            if unexpected_end_time is not None
            else f"UPDATE sleep_session ss SET end_time = '{end_time}' WHERE session_id = '{session_id}';"
        )

        with rds_conn.cursor() as cursor:
            cursor.execute(query)
            rds_conn.commit()

    except pymysql.MySQLError as e:
        logger.error("fails to update session end time", exc_info=e)
        raise e


def close_sessions(session_id: str, end_time: str, api_key: str, user_id: str, unexpected_end_time: str | None = None):
    try:
        body = (
            {"session_end_time": end_time}
            if unexpected_end_time is None
            else {"session_end_time": end_time, "unexpected": 1}
        )

        response = requests.post(
            url=f"https://api.asleep.ai/ai/v1/sessions/{session_id}/close",
            json=body,
            headers={"x-api-key": api_key, "x-user-id": user_id},
        )

        if response.status_code != 200:
            logger.error(f"fails to close session: {session_id}")

    except Exception as e:
        logger.error("fails to close session", exc_info=e)
        raise e


def modify_invalid_data(rds_conn: pymysql.connect, redis_conn: Redis):
    sessions = fetch_sessions_with_invalid_data(rds_conn)

    # sessions = [
    #     {
    #         "session_id": "20250114051103_zxuvb",
    #         "end_time": "2025-01-14T05:20:12Z",
    #         "unexpected_end_time": None,
    #         "api_key": "GbvW2UBfSLd7A67jDnngJJIsLwogR0r3KuFJZURW",
    #         "user_id": "G-20250114023526-qlRKOzQrMKZbqWVFiJPx",
    #     },
    # ]

    for session in sessions:
        remove_pp_and_stats(rds_conn, session["session_id"])
        remove_session_in_cache(redis_conn, session["session_id"])
        update_to_open(rds_conn, session["session_id"])
        close_sessions(
            session["session_id"],
            session["end_time"],
            session["api_key"],
            session["user_id"],
            session["unexpected_end_time"],
        )
        update_time(rds_conn, session["session_id"], session["end_time"], session["unexpected_end_time"])

        logger.info(f"successfully modified invalid data, session_id: {session['session_id']}")


def main():
    load_environments()
    create_rds_connections()
    create_redis_connection()

    redis_conn = get_redis_connection()
    rds_conn, _ = get_rds_connections()

    modify_invalid_data(rds_conn, redis_conn)


main()
