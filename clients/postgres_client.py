import psycopg2
from psycopg2 import sql
from psycopg2 import Error


class PostgresClient:
    def __init__(self):
        """Initialize connection parameters."""
        self.dbname = 'mydatabase'
        self.user = 'myuser'
        self.password = 'mypassword'
        self.host = 'localhost'
        self.port = '5432'
        self.connection = None
        self.cursor = None

    def connect(self):
        """Create a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connection to the database established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Execute a single query."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                print("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Fetch a single result from a query."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None