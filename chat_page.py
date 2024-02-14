# chat_page.py
import tkinter as tk

class ChatPage(tk.Frame):
    def __init__(self, parent, send_callback):
        super().__init__(parent)
        self.send_callback = send_callback
        self.create_widgets()

    def create_widgets(self):
        self.chat_log = tk.Text(self, state='disabled', height=20, width=50)
        self.chat_log.pack(pady=5)

        self.msg_entry = tk.Entry(self, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 5))

    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message:
            self.send_callback(message)
            self.msg_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)
