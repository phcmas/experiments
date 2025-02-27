import json
import logging
from numpy import real
import pymysql

from itertools import chain, count

from pymysql.cursors import DictCursor
from config.env_config import load_environments
from config.rds_config import create_rds_connections, get_rds_connections

logger = logging.getLogger(__name__)


def fetch_final_snorings(conn: pymysql.connect, session_id: str) -> list[dict]:
    try:
        query = f"""
        SELECT *
          FROM snoring_post_processing_result sppr
         WHERE sppr.session_id = "{session_id}";
        """

        with conn.cursor(DictCursor) as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return json.loads(row["result_list"])

    except pymysql.MySQLError as e:
        logger.error("fails to fetch final snorings", exc_info=e)
        raise e


def fetch_realtime_snorings(conn: pymysql.connect, session_id: str) -> list[dict]:
    try:
        query = f"""
        SELECT *
          FROM inference_stage is2
         WHERE is2.session_id = "{session_id}"
         ORDER BY is2.seq_num;
        """

        with conn.cursor(DictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return list(chain(*[json.loads(row["snoring_unit_list"]) for row in rows]))

    except pymysql.MySQLError as e:
        logger.error("fails to fetch final snorings", exc_info=e)
        raise e


def compare_snorings(conn: pymysql.connect, session_id: str) -> bool:
    logger.info(f"session_id: {session_id}")
    final_snorings = fetch_final_snorings(conn, session_id)
    realtime_snorings = fetch_realtime_snorings(conn, session_id)
    diffs = []

    for i, final_snoring, realtime_snoring in zip(count(), final_snorings, realtime_snorings):
        if final_snoring != realtime_snoring:
            logger.info(f"different, idx:{i}, realtime:{realtime_snoring}, final:{final_snoring}")
            diffs.append({"idx": i, "realtime": realtime_snoring, "final": final_snoring})

    logger.info(f"total length: {len(final_snorings)}, diff_count: {len(diffs)}")

    return str(realtime_snorings), str(final_snorings), diffs


def main():
    load_environments()
    create_rds_connections()

    conn, _ = get_rds_connections()

    result = {}
    session_ids = [
        "20250226170001_lci0x",
        "20241224174501_8pbch",
        "20241221183140_fr2o2",
        "20241225174502_xijtd",
        "20250121180004_vnkvv",
        "20250211173002_id4dl",
        "20250203180002_6w1ap",
    ]

    for session_id in session_ids:
        realtime, final, diffs = compare_snorings(conn, session_id)
        result[session_id] = {
            "total_length": len(final),
            "diff_count": len(diffs),
            "realtime_snorings": realtime,
            "final_snorings": final,
            "diffs": diffs,
        }

    with open("snoring.json", "w") as f:
        json.dump(result, f, indent=2)


main()
