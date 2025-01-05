import json
import logging

from alembic.op import f
import msgpack
import msgpack_numpy as m
import numpy as np
import pymysql
from pymysql.cursors import DictCursor

from config.env_config import load_environments
from config.rds_config import create_connections, get_connections

logger = logging.getLogger(__name__)

# restored = msgpack.unpackb(bytes, object_hook=m.decode)


def fetch_input_data_by_page(conn: pymysql.connect, limit: int, offset: int):
    try:
        query = f"""
        SELECT ss.session_id, ss.model_name, ppid.start_seq_num, ppid.sleep_stages, ppid.sleep_stage_logits,
               oppid.osas, oppid.osa_logits, sppid.snorings, sppid.snoring_logits
          FROM sleep_session ss
         INNER JOIN post_processing_input_data ppid on ss.session_id = ppid.session_id
         INNER JOIN osa_post_processing_input_data oppid on ppid.session_id = oppid.session_id and ppid.start_seq_num = oppid.start_seq_num
         INNER JOIN snoring_post_processing_input_data sppid on ppid.session_id = sppid.session_id and ppid.start_seq_num = sppid.start_seq_num
         WHERE ss.state = "OPEN"
           AND ss.start_time >= "2025-01-03 00:00:00"
         LIMIT {limit} OFFSET {offset};
        """

        with conn.cursor(DictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            {
                "session_id": row["session_id"],
                "model_name": row["model_name"],
                "start_seq_num": row["start_seq_num"],
                "sleep_stages": json.loads(row["sleep_stages"]),
                "sleep_stage_logits": json.loads(row["sleep_stage_logits"]),
                "osas": json.loads(row["osas"]),
                "osa_logits": json.loads(row["osa_logits"]),
                "snorings": json.loads(row["snorings"]),
                "snoring_logits": json.loads(row["snoring_logits"]),
            }
            for row in rows
        ]
    except pymysql.MySQLError as e:
        logger.error("fails to fetch input data", exc_info=e)
        raise e


def fetch_input_data(conn: pymysql.connect):
    rows, limit, offset = [], 10000, 0
    rows_by_page = fetch_input_data_by_page(conn, limit, offset)
    rows.extend(rows_by_page)

    while len(rows_by_page) > 0:
        offset += limit
        rows_by_page = fetch_input_data_by_page(conn, limit, offset)
        rows.extend(rows_by_page)

    return rows


def list_to_bin(s: list, dtype):
    return msgpack.packb(np.array(s, dtype=dtype), default=m.encode)


def bin_to_arr(bin):
    return msgpack.unpackb(bin, object_hook=m.decode)


def convert_for_db_insertion(input_data: dict):
    def get_end_mel_seq(start_mel_seq: int, model_name: str, sleep_stages: list):
        return min(start_mel_seq + 79, len(sleep_stages) - 1) if model_name == "highball" else start_mel_seq + 39

    return [
        (
            datum["session_id"],
            datum["start_seq_num"],
            datum["start_seq_num"] * 10,
            get_end_mel_seq(datum["start_seq_num"] * 10, datum["model_name"], datum["sleep_stages"]),
            list_to_bin(datum["sleep_stages"], np.uint8),
            list_to_bin(datum["sleep_stage_logits"], np.float32),
            list_to_bin(datum["osas"], np.uint8),
            list_to_bin(datum["osa_logits"], np.float32),
            list_to_bin(datum["snorings"], np.uint8),
            list_to_bin(datum["snoring_logits"], np.float32),
        )
        for datum in input_data
    ]


def save_model_prediction_by_page(conn: pymysql.connect, data: list):
    query = """
    INSERT IGNORE INTO model_prediction (session_id, prediction_seq, start_mel_seq, end_mel_seq, sleep_stages, sleep_stage_logits, osas, osa_logits, snorings, snoring_logits)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        with conn.cursor() as cursor:
            cursor.executemany(query, data)
            conn.commit()
    except pymysql.MySQLError as e:
        logger.error("fails to save model prediction", exc_info=e)
        raise e


def save_model_prediction(conn: pymysql.connect, data: list[tuple]):
    batch_size, offset = 1000, 0

    while offset < len(data):
        save_model_prediction_by_page(conn, data[offset : offset + batch_size])
        offset += batch_size

    logger.info("model predictions has been saved")


def fetch_model_prediction(conn: pymysql.connect):
    query = "SELECT * FROM model_prediction WHERE session_id = '20250105114803_3w32g'"

    with conn.cursor(DictCursor) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    for row in rows:
        logger.info(f"session_id:  {row['session_id']}")
        logger.info(f"prediction_seq: {row['prediction_seq']}")
        logger.info(f"start_mel_seq: {row['start_mel_seq']}")
        logger.info(f"end_mel_seq: {row['end_mel_seq']}")
        logger.info(f"sleep_stages: {bin_to_arr(row['sleep_stages'])}")
        logger.info(f"sleep_stage_logits: {bin_to_arr(row['sleep_stage_logits'])}")
        logger.info(f"osas: {bin_to_arr(row['osas'])}")
        logger.info(f"osa_logits: {bin_to_arr(row['osa_logits'])}")
        logger.info(f"snorings: {bin_to_arr(row['snorings'])}")
        logger.info(f"snoring_logits: {bin_to_arr(row['snoring_logits'])}")


def migrate_preds(conn: pymysql.connect, type: str = "main"):
    logger.info(f"migration of {type} has been started")

    raw_data = fetch_input_data(conn)
    converted_data = convert_for_db_insertion(raw_data)

    save_model_prediction(conn, converted_data)
    # fetch_model_prediction(conn)

    logger.info(f"migration of {type} has been completed")


def main():
    load_environments()
    create_connections()

    conn, test_conn = get_connections()

    migrate_preds(test_conn)
    # migrate_preds(conn)


main()
