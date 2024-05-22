import argparse
from gui import ChatbotGUI

def main():
    parser = argparse.ArgumentParser(description="Chatbot GUI Application")
    args = parser.parse_args()
    
    app = ChatbotGUI()
    app.run()

if __name__ == "__main__":
    main()
