
# Twilio WhatsApp integration

from flask import Flask, request, jsonify
import requests as pyrequests
from ai.chatbot import ChatBot
import os

app = Flask(__name__)

# Pilih AI provider yang diinginkan
# Untuk DeepSeek:
# chatbot = ChatBot(ai_provider="deepseek")
chatbot = ChatBot(ai_provider="deepseek")

# Konfigurasi Infobip
INFOBIP_BASE_URL = "https://38jd81.api.infobip.com"
INFOBIP_API_KEY = os.getenv("INFOBIP_API_KEY") or "7e19f87e7863bd18c1abf30ddd0293db-43c1f53d-cab0-4cba-952a-8a464223fbcf"
SENDER = "447860088970"  # Ganti dengan sender number Anda di Infobip

@app.route("/infobip-webhook", methods=["POST"])
def infobip_webhook():
    data = request.json
    # Cek struktur payload Infobip
    try:
        results = data.get("results", [])
        for result in results:
            from_number = result["from"]
            message_body = result["message"]['text']
            # Proses dengan ChatBot
            ai_reply = chatbot.generate_response(message_body)
            # Kirim balasan ke user via Infobip
            send_whatsapp_message_infobip(to=from_number, message=ai_reply)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

def send_whatsapp_message_infobip(to, message):
    url = f"{INFOBIP_BASE_URL}/whatsapp/1/message/text"
    headers = {
        'Authorization': f'App {INFOBIP_API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "from": SENDER,
        "to": to,
        "message": {
            "text": message
        }
    }
    response = pyrequests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    print("AI ChatBot WhatsApp via Infobip is running. Use ngrok to expose port 5000 or deploy to Render.")
    app.run(host="0.0.0.0", port=5000)