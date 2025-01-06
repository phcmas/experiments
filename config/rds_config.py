import logging

from config.env_config import get_environments
import pymysql

logger = logging.getLogger(__name__)
connection, test_connection = None, None


def create_rds_connections():
    env = get_environments()

    try:
        global connection, test_connection
        connection = pymysql.connect(
            host=env.RDS_HOST,
            port=env.RDS_PORT,
            user=env.RDS_USERNAME,
            password=env.RDS_PASSWORD,
            database="sleep",
        )
        test_connection = pymysql.connect(
            host=env.RDS_HOST,
            port=env.RDS_PORT,
            user=env.RDS_USERNAME,
            password=env.RDS_PASSWORD,
            database="sleep_test",
        )
    except pymysql.MySQLError as e:
        logger.error("fails to connect mysql")
        raise e


def get_rds_connections():
    global connection, test_connection
    return connection, test_connection


def close_rds_connections():
    if "connection" in locals() and connection.open:
        connection.close()

    if "connection" in locals() and test_connection.open:
        test_connection.close()

        logger.info("success to close connections")
