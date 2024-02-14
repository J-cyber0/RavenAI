import psycopg2
from psycopg2 import OperationalError
from .db_data_processing import DataProcessor  # Add this import statement

class DBManager:
    def __init__(self, postgres_host, postgres_db, postgres_user, postgres_password):
        self.postgres_host = postgres_host
        self.postgres_db = postgres_db
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password

    def connect_to_postgres(self):
        try:
            # Connect to PostgreSQL
            print("Connecting to PostgreSQL...")
            conn = psycopg2.connect(
                host=self.postgres_host,
                database=self.postgres_db,
                user=self.postgres_user,
                password=self.postgres_password
            )
            print("Connected to PostgreSQL!")
            return conn

        except OperationalError as e:
            print(f"Error: {e}")
            return None

    def create_postgres_tables(self):
        conn = self.connect_to_postgres()
        if conn:
            cursor = conn.cursor()
            # Define and execute table creation queries
            cursor.close()
            conn.close()

    def process_data(self):
        conn = self.connect_to_postgres()
        if conn:
            cursor = conn.cursor()
            # Example: Process data using functions from db_data_processing.py
            data_processor = DataProcessor()
            data_processor.process_data(cursor)
            cursor.close()
            conn.close()

if __name__ == "__main__":
    db_manager = DBManager(
        postgres_host='localhost',
        postgres_db='raven_main_db',
        postgres_user='postgres',
        postgres_password='#Wealth100',
    )
    db_manager.create_postgres_tables()
    db_manager.process_data()
