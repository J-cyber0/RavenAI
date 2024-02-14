import logging
import sys
import os
import pandas as pd
from openpyxl import load_workbook
from utils.github_api import GitHubAgent
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Document
)
from llama_index.core.readers.base import BaseReader

# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
sys.path.insert(0, 'c:/Users/marti/RavenAI')

agent = GitHubAgent

# Define a base class for custom readers with shared functionality
class CustomReader(BaseReader):
    def read_file(self, file, mode, encoding=None):
        try:
            with open(file, mode, encoding=encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read {file}: {e}")
            return None

class TxtReader(CustomReader):
    def load_data(self, file, extra_info=None):
        try:
            text = self.read_file(file, "r", encoding='utf-8')
            return [Document(text=text, extra_info=extra_info or {})] if text else []  
        except Exception as e:
            logger.error(f"Failed to load data from {file} as text: {e}")
            return []

class XlsxReader(CustomReader):
    def load_data(self, file, extra_info=None):
        try:
            text = self.read_file(file, "rb")  # Read in binary mode for pandas        
            if text:
                try:
                    dataframe = pd.read_excel(file)
                    csv_text = dataframe.to_csv(index=False)
                    return [Document(text=csv_text, extra_info=extra_info or {})]      
                except Exception as e:
                    logger.error(f"Failed to process {file} as Excel: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to load data from {file} as binary: {e}")
            return []

def main():
    PERSIST_DIR = "c:/Users/marti/RavenAI/storage"
    DOCUMENTS_DIRS = [
        "c:/Users/marti/RavenAI/Agents",
        "c:/Users/marti/RavenAI/Bots",
        "c:/Users/marti/RavenAI/Config",
        "c:/Users/marti/RavenAI/Data",
        "c:/Users/marti/RavenAI/gui",
        "c:/Users/marti/RavenAI/Scripts"  # Define your avoid list here
    ]

    try:
        index = initialize_index(PERSIST_DIR, DOCUMENTS_DIRS)
        if index:
            query_engine = index.as_query_engine()

            while True:
                user_input = input("User: ")
                if user_input.lower() == "exit":
                    break
                elif "github docs" in user_input.lower():
                    response = query_index(query_engine, user_input)
                    print("OpenAIBot:", response)
                elif "view repo" in user_input.lower():
                    response = query_index(query_engine,user_input)
                    print("OpenAIBot:", response)
                elif "view folder" in user_input.lower():
                    response = query_index(query_engine,user_input)
                    print("OpenAIBot:", response)
                else:
                    response = query_index(query_engine, user_input)
                    print("OpenAIBot:", response)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Exiting gracefully...")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


    finally:
        # Clean up resources if needed
        pass

# Function to initialize and load or reload the index
def initialize_index(persist_dir, document_dirs):
    AVOID_LIST = []  # Define your avoid list here
    try:
        if not os.path.exists(persist_dir):
            docs = []
            file_extractor = {
                ".txt": TxtReader(),
                ".xlsx": XlsxReader(),
                ".py": TxtReader()  # Add .py files
            }
            for directory in document_dirs:
                if os.path.isdir(directory):
                    reader = SimpleDirectoryReader(directory, recursive=True, exclude=AVOID_LIST, file_extractor=file_extractor)
                    docs.extend(reader.load_data(num_workers=6))
                else:
                    logger.warning(f"Skipping non-existent or non-directory: {directory}")
            index = VectorStoreIndex.from_documents(docs, persist_dir=persist_dir, show_progress=True, use_async=True)
            index.storage_context.persist(persist_dir=persist_dir)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)    
            index = load_index_from_storage(storage_context)
        return index
    except Exception as e:
        logger.error(f"Failed to initialize index: {e}")
        return None

# Function to query the index
def query_index(query_engine, query):
    try:
        if "github docs" in query.lower():
            # Extracting the link from the query
            link_start_index = query.lower().find("github docs") + len("github docs")
            link = query[link_start_index:].strip()
            
            # Passing the link to retrieve_github_docs function
            github_docs = agent.retrieve_github_docs(link)
            return github_docs
        else:
            response = query_engine.query(query)
            return response
    except Exception as e:
        logger.error(f"Failed to query index: {e}")
        return None

# Function to handle "view repo" command
def handle_view_repo(user_input):
    try:
        repo_name = user_input.lower().replace("view repo", "").strip()
        # Assuming the repo_name format is "owner/repo"
        owner, repo = repo_name.split('/')
        retrieve_and_display_repository_contents(owner, repo)
    except Exception as e:
        logger.error(f"Error handling view repo command: {e}")
        return None

# Function to handle "view folder" command
def handle_view_folder(user_input):
    try:
        folder_name = user_input.lower().replace("view folder", "").strip()
        # Assuming the folder_name format is "owner/repo/folder"
        owner, repo, directory = folder_name.split('/')
        retrieve_and_display_directory_contents(owner, repo, directory)
    except Exception as e:
        logger.error(f"Error handling view folder command: {e}")
        return None

# Function to retrieve and display repository contents
def retrieve_and_display_repository_contents(owner, repo):
    response = agent.retrieve_repository_contents(owner, repo)
    if response:
        if len(response) == 2:
            status, contents = response
            if contents:
                agent.view_repository_contents(contents)
            else:
                print("No contents found.")
        else:
            print("Unexpected response format:", response)
    else:
        print("Failed to retrieve repository contents.")


# Function to retrieve and display directory contents
def retrieve_and_display_directory_contents(owner, repo, directory):
    response = agent.retrieve_repository_contents(owner, repo)
    if response:
        status, contents = response
        if contents:
            for item in contents:
                if item['type'] == 'dir' and item['name'] == directory:
                    directory_contents = agent.retrieve_repository_contents(owner, repo, directory=item['path'])
                    if directory_contents:
                        status, contents = directory_contents
                        if contents:
                            agent.view_directory_contents(contents)
                        else:
                            print("No contents found in the directory.")
                    break
            else:
                print("Directory not found in the repository.")
        else:
            print("No contents found in the repository.")

if __name__ == "__main__":
    main()
