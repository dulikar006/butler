import json
import os
from clients.postgres_client import PostgresClient  # Assuming you saved the previous client code as postgres_py
# from models.order_model import Order  # Adjust the import according to your project structure


class PostgresManager(PostgresClient):

    def __init__(self):
        super().__init__()
        self.connect()

    def close(self):
        self.close()

    def store_order_table_row(self, name: str, description: str, criteria: str, customer_details: dict):
        """Store a new row in the PostgreSQL table."""
        try:
            # Convert customer_details dictionary to a JSON string
            customer_details_json = json.dumps(customer_details)

            insert_query = """
            WITH distinct_function AS (
                SELECT DISTINCT "function" 
                FROM actions 
                WHERE name = %s 
            )
            INSERT INTO orders (name, description, criteria, "function", customer_details)
            VALUES (%s, %s, %s, (SELECT "function" FROM distinct_function LIMIT 1), %s);
            """

            # Adjusting the parameter order
            self.execute_query(insert_query, (criteria, name, description, criteria, customer_details_json))
        except Exception as e:
            print(f"Error while storing table row: {e}")

    def get_order_table_data(self):
        """Retrieve all rows from the PostgreSQL table."""
        try:
            select_query = "SELECT * FROM orders;"
            data = self.fetch_all(select_query)
            dict_list = [
                {
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],  # Updated to include the description
                    "criteria": item[3],     # Updated to include the criteria
                    "function": item[4],
                    "customer_details": json.dumps(item[5]) if item[5] else None,  # Convert JSONB string to dict
                    "status": item[6],        # New status field
                    "created_at": item[7],    # New created_at field
                    "updated_at": item[8]     # New updated_at field
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

    def get_customer(self, phone_number):
        """Retrieve a customer by phone number using a raw SQL query and return as a dictionary."""
        try:
            # Define the SQL query
            select_query = """
                            SELECT * 
                            FROM customers 
                            WHERE phone_number = %s 
                            AND is_active = TRUE;
                        """

            # Use fetch_all to get the data
            data = self.fetch_all(select_query, (phone_number,))

            # Check if data is not empty
            if data:
                # Assuming the first row contains the desired customer
                customer = data[0]  # Fetch the first customer from the result

                # Map the result to a dictionary
                customer_dict = {
                    "id": customer[0],
                    "name": customer[1],
                    "phone_number": customer[2],
                    "room_number": customer[3],
                    "checkout_date": str(customer[4]),
                    "gender": customer[5],
                    "age": customer[6],
                    "family_members": customer[7],
                    "add_details": customer[8],
                    "is_active": customer[11],
                }
                return customer_dict
            else:
                return None

        except Exception as e:
            print(f"Error while fetching customer data: {e}")
            return None
