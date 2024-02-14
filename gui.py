import tkinter as tk
from tkinter import ttk
from .chat_page import ChatPage

class GUI:
    def __init__(self, master, display_response_callback):
        self.master = master
        self.display_response_callback = display_response_callback
        self.master.title("Raven AI")
        self.master.geometry("800x600")
        
        # Header Section
        header_label = tk.Label(master, text="Raven AI", font=("Helvetica", 20))
        header_label.pack(pady=10)
        
        # Navigation Bar
        navigation_frame = tk.Frame(master)
        navigation_frame.pack(fill="x")
        navigation_buttons = ["Home", "Chat", "Tasks", "Campaigns", "Calendar", "Files", "Settings", "Developer"]
        for btn_text in navigation_buttons:
            btn = tk.Button(navigation_frame, text=btn_text, padx=3, pady=1)
            btn.pack(side="left", padx=2, pady=2)
        
        # Main Content Area
        content_frame = tk.Frame(master)
        content_frame.pack(expand=True, fill="both")
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Add Tab Button
        self.add_tab_button = tk.Button(content_frame, text="New Chat", command=self.add_tab)
        self.add_tab_button.pack(side="left", padx=3, pady=1)
        
        # Delete Session Button
        self.delete_session_button = tk.Button(content_frame, text="Delete Session", command=self.delete_current_session)
        self.delete_session_button.pack(side="right", padx=3, pady=1)
        
        # Add initial tab
        self.add_tab()

    def init_ui(self):
        self.notebook = ttk.Notebook(self)
        self.chat_page = ChatPage(self.notebook, self.send_message_to_agent)
        self.notebook.add(self.chat_page, text="Chat")
        self.notebook.pack(expand=True, fill='both')

    def send_message_to_agent(self, message):
        # Placeholder for callback function to send message
        self.send_message_callback(message)

    def add_tab(self):
        new_tab_index = self.notebook.index(tk.END) + 1
        new_frame = ttk.Frame(self.notebook)
        self.notebook.add(new_frame, text=f"Session {new_tab_index}")
        chat_frame = tk.Frame(new_frame)
        chat_frame.pack(fill="both", expand=True)
        chat_history = tk.Text(chat_frame, height=20, width=50)
        chat_history.pack(fill="both", expand=True, padx=10, pady=10)
        chat_history.config(wrap="word")
        message_entry = tk.Entry(chat_frame, width=50)
        message_entry.pack(fill="x", padx=10, pady=5)
        message_entry.focus_set()
        send_button = tk.Button(chat_frame, text="Send", command=lambda: self.display_response_callback(new_tab_index, message_entry.get()))
        send_button.pack(side="right", padx=10, pady=5)
        message_entry.bind("<Return>", lambda event: send_button.invoke())
        # Store chat history widget in the frame for later retrieval
        new_frame.chat_history = chat_history
        new_frame.message_entry = message_entry

    def delete_tab(self, session_id):
        for tab_index in range(self.notebook.index(tk.END)):
            tab_widget = self.notebook.tabs()[tab_index]
            if self.notebook.tab(tab_widget, option="text") == f"Session {session_id}":
                self.notebook.forget(tab_widget)
                print(f"Deleted session {session_id}")
                break

    def delete_current_session(self):
        current_tab = self.notebook.select()
        current_session_id = int(self.notebook.tab(current_tab, option="text").split(" ")[1])
        self.delete_tab(current_session_id)

    def display_message(self, chat_history, user_input, response):
        print("Displaying message...")
        print("Chat history:", chat_history)
        if chat_history:
            chat_history.insert(tk.END, f"User: {user_input}\n")  # Display user input
            chat_history.insert(tk.END, f"Raven: {response}\n\n")  # Display Raven's response
            chat_history.see(tk.END)
        else:
            print("Error: Chat history is None")

    def display_error(self, chat_history, error_message):
        print("Displaying error...")
        print("Chat history:", chat_history)
        if chat_history:
            chat_history.insert(tk.END, f"Error: {error_message}\n\n")  # Display error message
            chat_history.see(tk.END)
        else:
            print("Error: Chat history is None")

    def get_chat_page_by_session(self, session_id):
        # Iterate over all tabs in the notebook
        for tab_index in range(self.notebook.index(tk.END)):
            tab_widget = self.notebook.nametowidget(self.notebook.tabs()[tab_index])
            tab_text = self.notebook.tab(tab_widget, option="text")
            # Check if the tab text contains the session ID
            if f"Session {session_id}" in tab_text:
                # Retrieve the chat history from the tab
                chat_history = tab_widget.chat_history
                if chat_history:
                    return chat_history
        # If no matching chat page is found, return None
        return None

    async def display_response(self, session_id, user_input):
        print("Received user input in session", session_id, ":", user_input)  # Debugging statement
        chat_page = self.get_chat_page_by_session(session_id)  # Use the correct method to get the ChatPage instance
        if chat_page is not None:
            chat_history = chat_page  # Assuming chat_history is accessible this way
            if user_input:
                # ... existing agent handling code remains unchanged
                try:
                    response = await self.current_agent.handle_input(user_input)
                    print("Generated response:", response)  # Debugging statement
                    chat_page.insert(tk.END, user_input + '\n')
                    chat_page.insert(tk.END, response + '\n')
                    chat_page.see(tk.END)
                except Exception as e:
                    print("An error occurred: {0}".format(e))  # Debugging statement
                    chat_page.insert(tk.END, f"An error occurred: {e}\n")
        else:
            print("No chat page found for session ID:", session_id)


def main():
    root = tk.Tk()
    app = GUI(root, None)
    root.mainloop()

if __name__ == "__main__":
    main()
