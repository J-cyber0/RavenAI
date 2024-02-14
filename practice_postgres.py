import psycopg2
from psycopg2 import OperationalError

def connect_to_postgres():
    try:
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            dbname="raven_main_db",
            user="postgres",
            password="#Wealth100",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL!")

        # Close the connection
        conn.close()
        print("Connection closed.")

    except OperationalError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_to_postgres()
