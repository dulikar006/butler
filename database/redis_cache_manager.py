import json

from clients.redis_client import RedisClient


class RedisCacheManager(RedisClient):

    def store_conversation(self, user_id, role, message_body, expire_time=360000):
        message = {
            'role': role,
            'body': message_body,
            'timestamp': '2024-09-27T10:00:00Z'  # Update as needed
        }
        key = f"conversation:{user_id}"
        self.connection.rpush(key, json.dumps(message))
        self.connection.expire(key, expire_time)  # Expiration time in seconds

    def get_conversation_history(self, user_id, limit=50):
        key = f"conversation:{user_id}"
        messages = self.connection.lrange(key, -limit, -1)
        return [json.loads(message) for message in messages]

    def display_conversation(self, user_id, limit=50):
        history = self.get_conversation_history(user_id, limit)
        for message in history:
            if message['role'] == 'user':
                print(f"User: {message['body']}")
            else:
                print(f"Agent: {message['body']}")
