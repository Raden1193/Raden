class WhatsAppIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "38jd81.api.infobip.com"

    def send_message(self, to, message):
        payload = {
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        response = self._make_request("POST", payload)
        return response

    def receive_message(self, request_data):
        # Logic to handle incoming messages
        from_number = request_data['from']
        message_body = request_data['body']
        return from_number, message_body

    def _make_request(self, method, payload):
        import requests
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, self.base_url, headers=headers, json=payload)
        return response.json()