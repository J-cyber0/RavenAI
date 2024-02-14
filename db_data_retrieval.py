class DataRetriever:
    def retrieve_data(self, cursor):
        try:
            # Execute SQL query to retrieve data from sample_table
            cursor.execute("SELECT * FROM sample_table")
            rows = cursor.fetchall()  # Fetch all rows

            # Print retrieved data
            print("Retrieved data from PostgreSQL:")
            for row in rows:
                print(row)

        except Exception as e:
            print(f"Error retrieving data: {e}")

if __name__ == "__main__":
    data_retriever = DataRetriever()
    # Assuming you have the cursor available here
    cursor = None  # Placeholder for cursor
    data_retriever.retrieve_data(cursor)
