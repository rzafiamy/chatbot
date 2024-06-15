import tkinter as tk
from tkinter import scrolledtext
import subprocess
from config import Config
from history import History

class ChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chatbot GUI")
        self.root.geometry(Config.WINDOW_SIZE)
        
        # System prompt label and text area
        self.system_prompt_label = tk.Label(self.root, text="System Prompt:", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.system_prompt_label.pack(padx=10, pady=5, anchor='w')
        self.system_prompt_text = tk.Text(self.root, height=5, font=(Config.FONT_FAMILY, Config.FONT_SIZE), wrap=tk.WORD)
        self.system_prompt_text.pack(padx=10, pady=5, fill=tk.X)
        self.system_prompt_text.insert(tk.END, "You are a helpful assistant to reply kindly to user")
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD, bg="white", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Define tags for styling user and bot messages
        self.chat_display.tag_config('user', background=Config.USER_BG, foreground=Config.USER_FG, font=Config.FONT_STYLE_USER)
        self.chat_display.tag_config('bot', background=Config.BOT_BG, foreground=Config.BOT_FG, font=Config.FONT_STYLE_BOT)
        
        # User input label and text area
        self.user_input_label = tk.Label(self.root, text="Your Message:", font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.user_input_label.pack(padx=10, pady=5, anchor='w')
        self.user_input_text = tk.Text(self.root, height=3, font=(Config.FONT_FAMILY, Config.FONT_SIZE), wrap=tk.WORD)
        self.user_input_text.pack(padx=10, pady=5, fill=tk.X)
        self.user_input_text.bind("<Return>", self.process_user_input)
        
        # Clear conversation button
        self.clear_button = tk.Button(self.root, text="Clear Conversation", command=self.clear_conversation, font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        self.clear_button.pack(padx=10, pady=5)

        self.history = History(Config.N - (Config.N * 0.1))
        
    def run(self):
        self.root.mainloop()
        
    def process_user_input(self, event):
        user_message = self.user_input_text.get("1.0", tk.END).strip()
        if user_message:
            if self.history.add_chat("<|user|>", user_message):
                self.display_message("You: " + user_message, "user")
                response = self.get_bot_response(user_message)
                self.display_message("Bot: " + response, "bot")
                self.user_input_text.delete("1.0", tk.END)
            else:
                self.display_message("Error: Not enough space to add new chat", "bot")
        return "break"  # Prevent default behavior of newline insertion
    
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

        command = [
            Config.SCRIPT_PATH,
            "--model", Config.MODEL_PATH,
            "-r", "User:",
            "--prompt", f"<|system|>\n{system_prompt}\n<|end|>\n{context}\n<|assistant|>\n",
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
            result =  result.stdout.strip()

            # Get only the part between the last <|assistant|> and <|end|> tags
            response = result.split("<|assistant|>")[-1].split("<|end|>")[0].strip()
            self.history.add_chat("<|assistant|>", response)
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
