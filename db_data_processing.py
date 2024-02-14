from .db_data_retrieval import DataRetriever

class DataProcessor:
    def process_data(self, cursor):
        # Instantiate DataRetriever
        data_retriever = DataRetriever()

        # Retrieve data from PostgreSQL using cursor
        postgres_data = data_retriever.retrieve_data(cursor)

        # Check if data is in a user-readable format
        if self.is_user_readable_format(postgres_data):
            print("Data is in user-readable format. Proceeding with processing...")
            self.process_postgres_data(postgres_data)
        else:
            print("Data is not in user-readable format. Skipping processing...")

    def is_user_readable_format(self, data):
        # Example function to check if data is in user-readable format
        # You can implement your own logic here
        return isinstance(data, list) and all(isinstance(row, dict) for row in data)

    def process_postgres_data(self, data):
        # Example: Process PostgreSQL data here
        processed_data = []
        for row in data:
            processed_row = {
                'id': row['id'],
                'name': row['name'],
                'age': row['age'],
                'email': row['email']
            }
            processed_data.append(processed_row)
        print("Processed data:", processed_data)

if __name__ == "__main__":
    data_processor = DataProcessor()
    # Assuming you have the cursor available here
    cursor = None  # Placeholder for cursor
    data_processor.process_data(cursor)
