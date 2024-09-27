import os

import redis


class RedisClient:

    def __init__(self):
        self.connection = None

    def connect(self):
        # Connect to Azure Redis Cache
        redis_host = os.environ['redis_url']
        redis_port = 6380  # Default port for SSL
        redis_password = os.environ['redis_key']

        # Create a Redis connection
        self.connection = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=True,  # Use SSL for security
            decode_responses=True  # To decode responses to strings
        )
