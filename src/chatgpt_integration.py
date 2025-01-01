# src/chatgpt_integration.py

import os
import requests

class ChatGPTClient:
    """
    A wrapper for ChatGPT integration.
    By default, uses the 'o1-mini' model, with an option to switch to 'chatgpt-01'.
    This could call the OpenAI API or an on-prem endpoint (depending on your deployment).
    """

    def __init__(self, api_key=None, endpoint=None, model=None):
        """
        Initialize the ChatGPT client.
        :param api_key: The API key for OpenAI (default: from environment variable CHATGPT_API_KEY).
        :param endpoint: The API endpoint for OpenAI (default: chat completions endpoint).
        :param model: The model to use (default: 'o1-mini'); can be overridden by environment variable CHATGPT_MODEL.
        """
        self.api_key = api_key or os.getenv("CHATGPT_API_KEY")
        self.endpoint = endpoint or "https://api.openai.com/v1/chat/completions"

        # Default to 'o1-mini' if no model is provided, unless overridden by environment var
        self.model = model or os.getenv("CHATGPT_MODEL", "o1-mini")

    def send_message(self, message: str, context: str = "") -> str:
        """
        Sends a prompt to the specified ChatGPT model and returns its response.
        :param message: The user's query.
        :param context: Additional context or system instructions.
        :return: The string response from the ChatGPT model.
        """
        if not self.api_key:
            raise ValueError("CHATGPT_API_KEY not set.")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"ChatGPT request failed: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
