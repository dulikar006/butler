import json
import unittest
from unittest.mock import MagicMock

from database.redis_cache_manager import RedisCacheManager


class TestRedisCacheManager(unittest.TestCase):

    def setUp(self):
        self.rcm = RedisCacheManager()
        self.rcm.connection = MagicMock()  # Mock the Redis connection

    def test_store_conversation(self):
        user_id = "user_12345"
        role = "user"
        message_body = "Hello, I need help with my booking."

        # When
        self.rcm.store_conversation(user_id, role, message_body)

        # Then: Ensure the message is stored correctly in Redis
        expected_message = {
            'role': role,
            'body': message_body,
            'timestamp': '2024-09-27T10:00:00Z'
        }
        self.rcm.connection.rpush.assert_called_once_with(
            f"conversation:{user_id}",
            json.dumps(expected_message)
        )

    def test_get_conversation_history(self):
        user_id = "user_12345"
        mock_messages = [
            json.dumps({'role': 'user', 'body': 'Hello!', 'timestamp': '2024-09-27T10:00:00Z'}),
            json.dumps({'role': 'agent', 'body': 'Hi there!', 'timestamp': '2024-09-27T10:01:00Z'}),
        ]

        # Mock the Redis lrange method to return mock messages
        self.rcm.connection.lrange.return_value = mock_messages

        # When
        history = self.rcm.get_conversation_history(user_id)

        # Then: Ensure the history is returned correctly
        expected_history = [
            {'role': 'user', 'body': 'Hello!', 'timestamp': '2024-09-27T10:00:00Z'},
            {'role': 'agent', 'body': 'Hi there!', 'timestamp': '2024-09-27T10:01:00Z'},
        ]
        self.assertEqual(history, expected_history)

    def test_display_conversation(self):
        user_id = "user_12345"
        mock_messages = [
            json.dumps({'role': 'user', 'body': 'Hello!', 'timestamp': '2024-09-27T10:00:00Z'}),
            json.dumps({'role': 'agent', 'body': 'Hi there!', 'timestamp': '2024-09-27T10:01:00Z'}),
        ]

        # Mock the Redis lrange method to return mock messages
        self.rcm.connection.lrange.return_value = mock_messages

        # Capture print output
        with unittest.mock.patch('builtins.print') as mocked_print:
            self.rcm.display_conversation(user_id)

            # Then: Ensure the printed output matches expectations
            mocked_print.assert_any_call("User: Hello!")
            mocked_print.assert_any_call("Agent: Hi there!")

if __name__ == '__main__':
    unittest.main()
