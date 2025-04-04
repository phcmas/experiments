from config.redis_config import create_redis_connection, get_redis_connection


if __name__ == "__main__":
    create_redis_connection()
    redis = get_redis_connection()

    channel = "test_channel"
