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
        self.connection.close()

    def get_conversation_history(self, user_id, limit=50):
        key = f"conversation:{user_id}"
        messages = self.connection.lrange(key, -limit, -1)
        self.connection.close()
        return [json.loads(message) for message in messages]

    def display_conversation(self, user_id, limit=50):
        history = self.get_conversation_history(user_id, limit)
        self.connection.close()
        for message in history:
            if message['role'] == 'user':
                print(f"User: {message['body']}")
            else:
                print(f"Agent: {message['body']}")

    def store_table_row(self, name, description):
        row_id = self.get_next_id()
        row_data = {
            "id": row_id,
            "name": name,
            "description": description
        }
        self.connection.rpush("table_data", json.dumps(row_data))
        self.connection.close()

    def get_next_id(self):
        table_data = self.get_table_data()
        return len(table_data) + 1

    def get_table_data(self):
        table_data = self.connection.lrange("table_data", 0, -1)
        self.connection.close()
        return [json.loads(row) for row in table_data]

    def delete_all_rows(self):
        self.connection.delete("table_data")
        self.connection.close()
