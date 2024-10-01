import os
from clients.postgres_client import PostgresClient  # Assuming you saved the previous client code as postgres_py
from models.order_model import Order  # Adjust the import according to your project structure

class OrderManager(PostgresClient):

    def __init__(self):
        super().__init__()
        self.connect()


    def close(self):
        self.close()

    def store_table_row(self, name: str, description: str, criteria: str):
        """Store a new row in the PostgreSQL table."""
        try:
            insert_query = """
            INSERT INTO orders (name, description, criteria) VALUES (%s, %s, %s);
            """
            self.execute_query(insert_query, (name, description, criteria))
        except Exception as e:
            print(f"Error while storing table row: {e}")

    def get_table_data(self):
        """Retrieve all rows from the PostgreSQL table."""
        try:
            select_query = "SELECT * FROM orders;"
            data = self.fetch_all(select_query)
            dict_list = [
                {
                    "id": item[0],
                    "name": item[1],
                    "details": eval(item[2]),  # Convert the string representation of a dict to an actual dict
                    "category": item[3]
                }
                for item in data
            ]
            return dict_list
        except Exception as e:
            print(f"Error while fetching table data: {e}")
            return None

    def delete_all_rows(self):
        """Delete all rows from the PostgreSQL table."""
        try:
            delete_query = "DELETE FROM orders;"
            self.execute_query(delete_query)
        except Exception as e:
            print(f"Error while deleting rows: {e}")

    def get_next_id(self):
        """Get the next available ID (auto-incremented in PostgreSQL)."""
        try:
            count_query = "SELECT COUNT(*) FROM orders;"
            result = self.fetch_one(count_query)
            return result[0] + 1 if result else 1
        except Exception as e:
            print(f"Error while getting the next ID: {e}")
            return None