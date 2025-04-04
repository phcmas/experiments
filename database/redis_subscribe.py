from config.redis_config import create_redis_connection, get_redis_connection


if __name__ == "__main__":
    create_redis_connection()
    redis = get_redis_connection()
    channel = "test_channel"

    pubsub = redis.pubsub()
    pubsub.subscribe(channel)

    print(f"subscribed to channel: {channel}")

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                print(f"received message: {message['data'].decode('utf-8')}")
    except KeyboardInterrupt:
        print("unsubscribing and exiting...")
        pubsub.unsubscribe(channel)
        pubsub.close()
