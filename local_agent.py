import os
import subprocess
import threading
import openpyxl
import docx
import PyPDF3
from raven_agent import RavenAgent  # Removed 'local_agent' import

class LocalAgent:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.processed_data = None
        self.thread = None

    def handle_input(self, user_input):
        if user_input.startswith("open "):
            full_path = user_input[5:]
            filename = os.path.basename(full_path)
            self.thread = threading.Thread(target=self.process_file, args=(full_path,))
            self.thread.start()
            self.thread.join()  # Wait for the processing thread to complete
            self.transfer_data_to_raven(filename)  # Call transfer_data_to_raven after processing
            return self.processed_data  # Return the processed data
        else:
            return "I'm sorry, I don't understand that command."

    def retrieve_and_clean_data(self, filename):
        return self.file_handler.retrieve_and_clean_data(filename)

    def process_file(self, filename):
        try:
            print("Processing file:", filename)  # Add logging for debugging
            self.processed_data = self.read_file(filename)
            return self.format_data(self.processed_data)  # Format the data before returning
        except Exception as e:
            self.processed_data = f"An error occurred: {e}"
            print("Error processing file:", e)  # Add logging for debugging
            return self.processed_data

    def format_data(self, data):
        if isinstance(data, list):
            formatted_data = ""
            for row in data:
                formatted_data += ", ".join(str(cell) for cell in row) + "\n"
            return formatted_data
        else:
            return data

    @staticmethod
    def read_file(filename):
        file_extension = os.path.splitext(filename)[1].lower()
        try:
            if file_extension == '.xlsx':
                return LocalAgent.read_excel_file(filename)
            elif file_extension == '.docx':
                return LocalAgent.read_docx_file(filename)
            elif file_extension == '.pdf':
                return LocalAgent.read_pdf_file(filename)
            elif file_extension == '.txt':
                return LocalAgent.read_text_file(filename)
            else:
                return "Unsupported file type."
        except FileNotFoundError:
            return f"File '{filename}' not found."
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def read_excel_file(filename, sheet_name='Sheet1'):
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook[sheet_name]
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        return data

    @staticmethod
    def read_docx_file(filename):
        doc = docx.Document(filename)
        file_contents = ''
        for para in doc.paragraphs:
            file_contents += para.text + '\n'
        return file_contents

    @staticmethod
    def read_pdf_file(filename):
        with open(filename, 'rb') as file:
            reader = PyPDF3.PdfFileReader(file)
            file_contents = ''
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                file_contents += page.extractText()
        return file_contents

    @staticmethod
    def read_text_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        return file_contents

    def transfer_data_to_raven(self, filename):
        if self.processed_data is not None:
            RavenAgent.receive_data(self.processed_data)
            self.processed_data = None  # Reset processed data after transfer
            print(f"Data from {filename} transferred to RavenAgent.")
        else:
            print("No data to transfer.")

    def is_processing(self):
        return self.thread is not None and self.thread.is_alive()

    def execute_local_command(self, command):
        # Execute a local command
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            return str(e)

    def get_processed_data(self):
        return self.processed_data

    def is_processing(self):
        return self.thread is not None and self.thread.is_alive()

# Example usage (removed from LocalAgent script)
# if __name__ == "__main__":
#     user_input = input("Enter a command: ")
#     response = raven_agent.handle_input(user_input)
#     print("Agent:", response)
