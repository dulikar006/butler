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
