import tkinter as tk
import os
import google.generativeai as genai
from ..Config import config
from ..Agents import raven_agent, file_handler
from ..gui.gui import GUI
from ..Scripts.db_management import DBManager

# Set up your API key
genai.configure(api_key=os.environ.get('GOOG_GEMINI_API_KEY'))

class ChatSession:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-pro')  # Adjust this line as per actual library usage
        self.chat = self.model.start_chat()  # Start a chat session

    def send_message(self, content, stream=False):
        try:
            response = self.chat.send_message(content, stream=stream)
            return response.text if not stream else ''.join([chunk.text for chunk in response])
        except Exception as e:
            print(f"Error sending message to model: {e}")
            return "Error occurred while processing your request."

    def rewind(self):
        # Removes the last request/response pair from the chat history.
        return self.chat.rewind()

class Raven:
    def __init__(self, master):
        self.master = master
        master.title("Raven")
        self.setup_agents()
        self.gui = GUI(master, self.display_response)
        self.current_agent = self.default_agent
        self.chat_histories = {}  # Dictionary to store chat histories for different sessions

    def setup_agents(self):
        self.chat_session = ChatSession()
        self.file_handler = file_handler.FileHandler()
        self.db_manager = DBManager(
            postgres_host=config.PG_HOST,
            postgres_db=config.PG_DB,
            postgres_user=config.PG_USER,
            postgres_password=config.PG_PASS
            # MongoDB arguments are optional and can be omitted
        )
        self.default_agent = raven_agent.RavenAgent(self.chat_session, self.file_handler, self.db_manager)

    def display_response(self, session_id, user_input):
        print("Received user input in session", session_id, ":", user_input)  # Debugging statement
        chat_page = self.gui.get_chat_page_by_session(session_id)  # Use the correct method to get the ChatPage instance
        if chat_page is not None:
            chat_history = chat_page  # Assuming chat_history is accessible this way
            if user_input:
                try:
                    # Process user input using RavenAgent
                    raven_response = self.current_agent.handle_input(user_input)

                    # Process user input using OpenAIBot
                    openai_response = self.chat_session.send_message(user_input)

                    # Determine which response is better
                    better_response = self.determine_better_response(raven_response, openai_response)

                    # Display the better response in chat history
                    chat_history.insert(tk.END, "You: " + user_input + '\n')
                    chat_history.insert(tk.END, "Raven: " + better_response + '\n')
                    chat_history.see(tk.END)
                except Exception as e:
                    print("An error occurred: {0}".format(e))  # Debugging statement
                    chat_history.insert(tk.END, f"An error occurred: {e}\n")
        else:
            print("No chat page found for session ID:", session_id)

    def determine_better_response(self, response1, response2):
        # Example: Simply compare lengths of responses
        if len(response1) >= len(response2):
            return response1
        else:
            return response2

# Part of your main application initialization
def main():
    root = tk.Tk()
    raven = Raven(root)  # Pass the root window as the master argument
    root.mainloop()

if __name__ == "__main__":
    main()
