

import os
from dotenv import load_dotenv
load_dotenv()

# Optional imports
try:
    import cohere
except ImportError:
    cohere = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None
import requests as pyrequests

class ChatBot:
    def __init__(self, ai_provider="cohere", api_key=None):
        """
        ai_provider: "cohere", "huggingface", or "none"
        api_key: override API key (optional)
        """
        self.responses = {
            "hi": "Hello! How can I assist you today?",
            "bye": "Goodbye! Have a great day!",
            "how are you?": "I'm just a program, but thanks for asking!",
        }
        self.ai_provider = ai_provider.lower()
        self.api_key = api_key
        # Load API keys from env if not provided
        self.cohere_api_key = api_key or os.getenv("COHERE_API_KEY")
        self.gemini_api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.deepseek_api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        # Setup for each provider
        if self.ai_provider == "cohere" and cohere and self.cohere_api_key:
            self.cohere_client = cohere.Client(self.cohere_api_key)
        elif self.ai_provider == "gemini" and genai and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        # DeepSeek tidak perlu inisialisasi khusus


    def process_input(self, user_input):
        user_input = user_input.lower()
        return self.responses.get(user_input, "I'm sorry, I don't understand that.")

    def generate_response(self, user_input):
        if self.ai_provider == "cohere" and cohere and self.cohere_api_key:
            try:
                response = self.cohere_client.generate(
                    model="command", prompt=user_input, max_tokens=100
                )
                return response.generations[0].text.strip()
            except Exception as e:
                return f"Cohere error: {str(e)}"
        elif self.ai_provider == "gemini" and genai and self.gemini_api_key:
            try:
                response = self.gemini_model.generate_content(user_input)
                return response.text.strip()
            except Exception as e:
                return f"Gemini error: {str(e)}"
        elif self.ai_provider == "deepseek" and self.deepseek_api_key:
            try:
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                }
                resp = pyrequests.post(url, headers=headers, json=payload, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return f"DeepSeek error: {str(e)}"
        else:
            return self.process_input(user_input)
    