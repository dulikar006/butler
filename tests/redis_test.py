import json

import redis

class RedisClient:

    def __init__(self):
        self.connection = None

    def connect(self):
        # Connect to Azure Redis Cache
        redis_host = 'butler-redis-cache.redis.cache.windows.net'
        redis_port = 6380  # Default port for SSL
        redis_password = 'Ml6HNBdQWhN4jjgmpT2586tX1YMkxipacAzCaKABv9g='

        # Create a Redis connection
        self.connection = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=True,  # Use SSL for security
            decode_responses=True  # To decode responses to strings
        )

    def is_order_creation(self, user_id, limit=50):
        key = f"order_:{user_id}"
        messages = self.connection.lrange(key, -limit, -1)
        self.connection.close()
        return [json.loads(message) for message in messages]

    def delete_order_creation(self, user_id):
        key = f"order_:{user_id}"
        self.connection.delete(key)
        self.connection.close()

# sms_sid = 'AC7ace3468f7e53936b2c49e16ad354814'
# redis_manager = RedisClient()
# redis_manager.connect()
# print(redis_manager.is_order_creation(sms_sid))
# redis_manager.delete_order_creation(sms_sid)