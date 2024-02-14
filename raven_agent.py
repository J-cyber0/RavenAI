import os
from ..utils.github_api import GitHubAgent
from ..Bots.raven import ChatSession
from ..Scripts.db_management import DBManager

class RavenAgent:
    data = None  # Class variable to store received data

    def __init__(self, chat_session, file_handler, db_manager):
        self.chat_session = chat_session
        self.file_handler = file_handler
        self.db_manager = db_manager
        self.metadata = {
            "name": "RavenAgent",
            "version": "1.0",
            "description": "Generative AI based agent"
        }
        self.repository_summaries = []  # List to store summaries

    def setup_ui(self, gui):
        self.gui = gui

    def handle_input(self, user_input):
        # Handle the 'scan' command
        if user_input.startswith('scan '):
            url = user_input.split(' ', 1)[1]
            if "github.com" in url:
                message, data = GitHubAgent.retrieve_github_docs(url)
                if data:
                    # Create a summary from the repository data
                    summary = self.create_summary(data)
                    # Add the summary to the list
                    self.repository_summaries.append(summary)
                    return "Repository scanned successfully. Summary saved."
                return message
            else:
                return "Invalid GitHub URL."
        # Handle the 'view summaries' command
        elif user_input == 'view summaries':
            return self.view_summaries()
        # Handle the 'call db' command
        elif user_input == 'call db':
            return self.call_db_manager()
        # Handle GitHub-related commands
        elif "github docs" in user_input.lower():
            link_start_index = user_input.lower().find("github docs") + len("github docs")
            link = user_input[link_start_index:].strip()
            response = GitHubAgent.retrieve_github_docs(link)
            if response:
                return response
            else:
                return "Failed to retrieve GitHub documentation."
        elif user_input.startswith('scan '):
            link = user_input.split(' ', 1)[1]
            if "github repo" in url:
                return GitHubAgent.retrieve_repository_contents(link)
        elif "view repo" in user_input.lower():
            link = user_input.split(' ', 1)[1]
            return GitHubAgent.view_repository_contents(link)
        elif "view dir" in user_input.lower():
            link = user_input.split(' ', 1)[1]
            return GitHubAgent.view_repository_contents(link)
        else:
            # Process other inputs
            response = self.chat_session.send_message(user_input)
            return response

    def create_summary(self, data):
        # Create a summary based on the desired information
        summary = {
            "name": data.get("name", "No name available"),
            "description": data.get("description", "No description provided."),
            "stars": data.get("stargazers_count", 0)
        }
        return summary
    
    # Add a method to view saved summaries
    def view_summaries(self):
        if not self.repository_summaries:
            return "No summaries available."
        summaries_text = "\n\n".join([f"Name: {summary['name']}, Description: {summary['description']}, Stars: {summary['stars']}" for summary in self.repository_summaries])
        return summaries_text

    # New method to call DBManager
    def call_db_manager(self):
        # Assuming you have some method in DBManager to perform certain database operations
        # For example:
        try:
            self.db_manager.process_data()
            return "Database operation successful."
        except Exception as e:
            return f"Error while performing database operation: {e}"

    # Other methods remain unchanged
