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

    '''to keep on track if normal conversation or order creation'''
    def add_is_order_creation(self, user_id, order_Type, expire_time=3600):
        key = f"order_:{user_id}"
        self.connection.rpush(key, json.dumps(order_Type))
        self.connection.expire(key, expire_time)  # Expiration time in seconds
        self.connection.close()
    def is_order_creation(self, user_id, limit=50):
        key = f"order_:{user_id}"
        messages = self.connection.lrange(key, -limit, -1)
        self.connection.close()
        return [json.loads(message) for message in messages]

    def delete_order_creation(self, user_id):
        key = f"order_:{user_id}"
        self.connection.delete(key)
        self.connection.close()
    '''order_creation_helper_ends_here'''


    '''to check if a customer'''
    def add_is_customer(self, phone_number, details, expire_time=3600):
        key = f"customer_:{phone_number}"
        self.connection.rpush(key, json.dumps(details))
        self.connection.expire(key, expire_time)  # Expiration time in seconds
        self.connection.close()
    def is_customer(self, phone_number, limit=50):
        key = f"customer_:{phone_number}"
        messages = self.connection.lrange(key, -limit, -1)
        self.connection.close()
        return [json.loads(message) for message in messages]

    def delete_customer(self, phone_number):
        key = f"customer_:{phone_number}"
        self.connection.delete(key)
        self.connection.close()
    '''customer check_helper_ends_here'''

    # def store_table_row(self, name, description, criteria):
    #     row_id = self.get_next_id()
    #     row_data = {
    #         "id": row_id,
    #         "name": name,
    #         "description": description,
    #         "criteria": criteria
    #     }
    #     self.connection.rpush("table_data", json.dumps(row_data))
    #     self.connection.close()
    #
    # def get_next_id(self):
    #     table_data = self.get_table_data()
    #     return len(table_data) + 1
    #
    # def get_table_data(self):
    #     table_data = self.connection.lrange("table_data", 0, -1)
    #     self.connection.close()
    #     return [json.loads(row) for row in table_data]
    #
    # def delete_all_rows(self):
    #     self.connection.delete("table_data")
    #     self.connection.close()

    def delete_all(self):
        self.connection.flushdb()  # Deletes all keys from the current database
        self.connection.close()


