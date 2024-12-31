# src/chatgpt_integration.py

import os
import requests

class ChatGPTClient:
    """
    A wrapper for ChatGPT-01 integration.
    This could call the OpenAI API or an on-prem endpoint
    (depending on your deployment).
    """

    def __init__(self, api_key=None, endpoint=None):
        self.api_key = api_key or os.getenv("CHATGPT_API_KEY")
        self.endpoint = endpoint or "https://api.openai.com/v1/chat/completions"
    
    def send_message(self, message: str, context: str = "") -> str:
        """
        Sends a prompt to the ChatGPT-01 model and returns its response.
        :param message: The user query.
        :param context: Additional context or system instructions.
        :return: The string response from ChatGPT-01.
        """
        if not self.api_key:
            raise ValueError("CHATGPT_API_KEY not set.")

        payload = {
            "model": "gpt-3.5-turbo",  
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
            raise RuntimeError(f"ChatGPT-01 request failed: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
