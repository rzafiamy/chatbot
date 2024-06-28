import tkinter as tk
from tkinter import scrolledtext
import subprocess
from config import Config
from history import History
from chat_template import ChatTemplate
from session import Session
import os

class ChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chatbot GUI")
        self.root.geometry(Config.WINDOW_SIZE)
        
        # Initialize current session ID and session object
        self.current_session_id = None
        self.session = None
        
        # Left side panel for sessions
        self.sessions_frame = tk.Frame(self.root, width=200, bg="lightgray")
        self.sessions_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.sessions_label = tk.Label(self.sessions_frame, text="Sessions", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.sessions_label.pack(pady=10)
        
        self.sessions_listbox = tk.Listbox(self.sessions_frame, width=30, height=20)
        self.sessions_listbox.pack(padx=10, pady=10)
        self.sessions_listbox.bind('<<ListboxSelect>>', self.on_session_select)
        
        self.add_session_button = tk.Button(self.sessions_frame, text="Add Session", command=self.add_session)
        self.add_session_button.pack(side=tk.BOTTOM, padx=10, pady=5, fill=tk.X)
        
        self.delete_session_button = tk.Button(self.sessions_frame, text="Delete Session", command=self.delete_session)
        self.delete_session_button.pack(side=tk.BOTTOM, padx=10, pady=5, fill=tk.X)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, bg="white", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.chat_display.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # System prompt label and text area
        self.system_prompt_label = tk.Label(self.root, text="System Prompt:", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.system_prompt_label.pack(padx=10, pady=5, anchor='w')
        self.system_prompt_text = tk.Text(self.root, height=5, font=(Config.FONT_FAMILY, Config.FONT_SIZE), wrap=tk.WORD)
        self.system_prompt_text.pack(padx=10, pady=5, fill=tk.X)
        self.system_prompt_text.insert(tk.END, "You are a helpful assistant to reply kindly to user")
        
        # User input label and text area
        self.user_input_label = tk.Label(self.root, text="Your Message:", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.user_input_label.pack(padx=10, pady=5, anchor='w')
        self.user_input_text = tk.Text(self.root, height=3, font=(Config.FONT_FAMILY, Config.FONT_SIZE), wrap=tk.WORD)
        self.user_input_text.pack(padx=10, pady=5, fill=tk.X)
        self.user_input_text.bind("<Return>", self.process_user_input)
        
        # Clear conversation button
        self.clear_button = tk.Button(self.root, text="Clear Conversation", command=self.clear_conversation, font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.clear_button.pack(padx=10, pady=5)
        
        # Initialize history and chat template
        self.history = History(Config.N - (Config.N * 0.1))
        self.chat_template = ChatTemplate()
        
        # Load existing sessions
        self.load_sessions()
        self.update_sessions_listbox()
        
        # Select the first session by default
        if self.available_sessions:
            self.current_session_id = self.available_sessions[0]
            self.load_session()
        
    def run(self):
        self.root.mainloop()
        
    def process_user_input(self, event):
        user_message = self.user_input_text.get("1.0", tk.END).strip()
        if user_message:
            if self.history.add_chat("", user_message):
                self.display_message("You: " + user_message, "user")
                response = self.get_bot_response(user_message)
                self.display_message("Bot: " + response, "bot")
                self.user_input_text.delete("1.0", tk.END)

                self.session.add_message("user", user_message)
                self.session.add_message("bot", response)
                self.session.save()
            else:
                self.display_message("Error: Not enough space to add new chat", "bot")
        return "break"  # Prevent default behavior of newline insertion
    
    def load_sessions(self):
        self.available_sessions = []
        session_files = os.listdir("session")
        for file in session_files:
            if file.endswith(".fi"):
                session_id = int(file.split("_")[1].split(".")[0])
                self.available_sessions.append(session_id)

    def update_sessions_listbox(self):
        self.sessions_listbox.delete(0, tk.END)
        for session_id in self.available_sessions:
            self.sessions_listbox.insert(tk.END, f"Session {session_id}")

    def on_session_select(self, event):
        index = self.sessions_listbox.curselection()
        if index:
            selected_session = self.sessions_listbox.get(index)
            session_id = int(selected_session.split()[1])
            if session_id != self.current_session_id:
                self.current_session_id = session_id
                self.clear_conversation()
                self.load_session()
                
    def load_session(self):
        self.session = Session.load(self.current_session_id)
        if not self.session:
            messagebox.showerror("Session Error", f"Session {self.current_session_id} not found or deleted.")
            self.current_session_id = None
        # display messages
        for message in self.session.messages:
            # access tuple elements
            sender, text = message
            self.display_message(f"{sender.capitalize()}: {text}", sender)
    
    def add_session(self):
        new_session_id = max(self.available_sessions) + 1 if self.available_sessions else 1
        self.current_session_id = new_session_id
        self.session = Session(new_session_id)
        self.session.save()
        self.available_sessions.append(new_session_id)
        self.update_sessions_listbox()
        self.sessions_listbox.selection_clear(0, tk.END)
        self.sessions_listbox.selection_set(tk.END)
        self.sessions_listbox.activate(tk.END)
        self.clear_conversation()

    def delete_session(self):
        if self.session:
            self.session.delete()
            messagebox.showinfo("Session Deleted", "Session has been deleted")
            self.current_session_id  = 1
            self.load_session()
    
    def display_message(self, message, sender):
        self.chat_display.config(state='normal')
        if sender == "user":
            self.chat_display.insert(tk.END, "\n" + message + "\n", "user")
        else:
            self.chat_display.insert(tk.END, "\n" + message + "\n", "bot")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)
    
    def get_bot_response(self, message):
        system_prompt = self.system_prompt_text.get("1.0", tk.END).strip()

        context = self.history.get_context()

        formatted_prompt = self.chat_template.format_prompt(system_prompt, message, context)

        command = [
            Config.SCRIPT_PATH,
            "--model", Config.MODEL_PATH,
            "-r", "User:",
            "--prompt", formatted_prompt,
            "-ngl", str(Config.NGL),
            "-b", str(Config.BATCH),
            "-n", str(Config.N),
            "--temp", str(Config.TEMPERATURE),
            "-e",
            "-c", str(Config.C),
            "--repeat_penalty", str(Config.REPEAT_PENALTY)
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            raw_response = result.stdout.strip()
            response = self.chat_template.format_response(raw_response)
            self.history.add_chat("", response)
            return response
        except Exception as e:
            return f"Error: {e}"

    def clear_conversation(self):
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        self.history = History(Config.N - (Config.N * 0.1))

if __name__ == "__main__":
    app = ChatbotGUI()
    app.run()
