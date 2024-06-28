import os
import pickle

class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.messages = []  # Placeholder for messages in the session

    @classmethod
    def load(cls, session_id):
        session_file = f"session/session_{session_id}.fi"
        if os.path.exists(session_file):
            with open(session_file, 'rb') as f:
                return pickle.load(f)
        else:
            return cls(session_id)

    def save(self):
        session_file = f"session/session_{self.session_id}.fi"
        with open(session_file, 'wb') as f:
            pickle.dump(self, f)

    def delete(self):
        session_file = f"session/session_{self.session_id}.fi"
        if os.path.exists(session_file):
            os.remove(session_file)
    
    def add_message(self, sender, message):
        self.messages.append((sender, message))

    def get_messages(self):
        return self.messages
