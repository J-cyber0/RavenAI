import os
import tkinter as tk
import google.generativeai as genai
from Agents import raven_agent, local_agent

# Set up your API key
genai.configure(api_key=os.environ['GOOG_GEMINI_API_KEY'])

class Raven:
    def __init__(self, master):
        self.master = master
        master.title("Raven")
        self.setup_gui()
        self.setup_agents()
        self.current_agent = self.default_agent  # Set Raven AI as the default agent

    def setup_agents(self):
        # Initialize GenerativeModel
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_session = self.model.start_chat()

        # Initialize Raven agent
        self.raven = raven_agent.RavenAgent(self.chat_session)

        # Initialize LocalAgent
        self.local_agent = local_agent.LocalAgent()

        # Set default agent
        self.default_agent = self.raven  # Default agent is the Raven agent

    def setup_gui(self):
        # Configure resizing behavior
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create chat history display area
        self.chat_history = tk.Text(self.master, height=20, width=50)
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create input field for user messages
        self.message_entry = tk.Entry(self.master, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.message_entry.focus_set()

        # Bind Return key to display_response method
        self.message_entry.bind("<Return>", lambda event: self.display_response())

        # Configure resizing behavior
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def display_response(self):
        user_input = self.message_entry.get().strip()
        if user_input:
            # Check if the user input starts with '@' to switch agents
            if user_input.startswith("@"):
                agent_name = user_input[1:].lower()
                if agent_name == "raven":
                    self.current_agent = self.raven
                elif agent_name == "localagent":
                    self.current_agent = self.local_agent
                else:
                    self.chat_history.insert(tk.END, "Unknown agent. Please specify 'Raven' or 'LocalAgent'.\n\n")
                self.message_entry.delete(0, tk.END)
                return
            try:
                # Use the current agent to handle the user input
                response = self.current_agent.handle_input(user_input)
                self.chat_history.insert(tk.END, f"You: {user_input}\nAgent: {response}\n\n")
            except Exception as e:
                self.chat_history.insert(tk.END, f"An error occurred: {e}\n\n")

def main():
    root = tk.Tk()
    app = Raven(root)
    root.mainloop()

if __name__ == "__main__":
    main()
