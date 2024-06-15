class History:
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens
        self.history = []
        self.current_tokens = 0

    def __normalize(self, message):
        """
        Normalizes the message by removing leading and trailing whitespaces and converting it to lowercase.
        """
        message = message.strip().lower()

        # replace multiple spaces with a single space or multiple newlines with a single newline
        message = ' '.join(message.split())

        return message

    def add_chat(self, sender, message):
        """
        Adds a chat to the history.
        If adding the chat would exceed max_tokens, it removes the oldest chats first.
        """
        # Calculate tokens in new message
        new_tokens = len(message.split())
        while self.current_tokens + new_tokens > self.max_tokens and self.history:
            removed_sender, removed_message = self.history.pop(0)
            self.current_tokens -= len(removed_message.split())
        
        # Append new message if space is available
        if self.current_tokens + new_tokens <= self.max_tokens:
            self.history.append((sender, self.__normalize(message)))
            self.current_tokens += new_tokens
            return True
        else:
            print("Not enough space to add new chat")
            return False

    def get_context(self):
        """
        Returns all conversations formatted as 'user: message, bot: message,...'
        """
        ctx = "\n".join(f"{sender}\n{message}<|end|>" for sender, message in self.history)
        # print(ctx)
        return ctx

if __name__ == "__main__":
    # Example of using the History class
    history = History(50)  # Limiting the buffer to 50 tokens
    history.add_chat('user', "Hello, how are you?")
    history.add_chat('bot', "I'm fine, thank you! And you?")
    history.add_chat('user', "I'm good, thanks for asking!")

    print(history.get_context())
