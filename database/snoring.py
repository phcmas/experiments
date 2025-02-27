from config.env_config import load_environments
from config.rds_config import create_rds_connections, get_rds_connections


def main():
    load_environments()
    create_rds_connections()

    conn, test_conn = get_rds_connections()


main()
