import requests

class TelegramIntegration:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = f"https://api.telegram.org/bot{api_token}/"

    def send_message(self, chat_id, text):
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, json=payload)
        return response.json()

    def receive_updates(self):
        url = f"{self.base_url}getUpdates"
        response = requests.get(url)
        return response.json()

    def process_message(self, message):
        chat_id = message['chat']['id']
        text = message['text']
        # Here you can add logic to process the message and generate a response
        response_text = f"You said: {text}"
        self.send_message(chat_id, response_text)