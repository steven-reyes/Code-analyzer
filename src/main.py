# src/main.py

import json
import os

from src.config.settings_loader import load_settings
from src.modules.example_module import greet_user
from src.utils.file_utils import read_file
from src.chatgpt_integration import ChatGPTClient

# <-- Import your Flask app if you have one in src/ui/app.py
from src.ui.app import app  # e.g., "app = Flask(__name__)" is defined here

def main():
    """
    Main entry point for the Code Analyzer application.
    Orchestrates basic logic: config loading, greetings, file reading, ChatGPT usage,
    and optionally starts a Flask server if you want local hosting on port 5000.
    """
    # Load settings
    config = load_settings()

    # Greet user
    user_greeting = greet_user("Alice")
    print(user_greeting)

    # Example usage: read a file
    file_contents = read_file("some_data_file.txt")
    if file_contents:
        print("File read successfully!\n", file_contents)

    # Print loaded config
    print("Main application is running with the following config:")
    print(json.dumps(config, indent=2))

    # Demonstrate ChatGPT-01 integration
    chatgpt_client = ChatGPTClient()
    user_query = "What can you tell me about the project structure?"
    response = chatgpt_client.send_message(
        user_query,
        context="You are ChatGPT-01. Provide insights on code structure."
    )
    print("ChatGPT-01 Response:", response)

    # Start the Flask app on localhost:5000
    print("Starting Flask server on http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    main()
