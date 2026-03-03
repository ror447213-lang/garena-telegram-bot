import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔐 YAHAN APNA NEW BOT TOKEN DALO
BOT_TOKEN = "8707631665:AAHF7p5vMOu3qlTcZ0MXTjOKMojlk1rDnsI"

API_BASE = "https://email-checke38.vercel.app"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.route("/", methods=["GET"])
def home():
    return "Bot Running 24/7", 200


@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return "ok"

        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text.startswith("/start"):
            send(chat_id, "🤖 Bot Active\n\nUse:\n/bind ACCESS_TOKEN\n/health")

        elif text.startswith("/health"):
            send(chat_id, "🟢 Server Running")

        elif text.startswith("/bind"):
            parts = text.split(" ")

            if len(parts) < 2:
                send(chat_id, "Usage:\n/bind ACCESS_TOKEN")
            else:
                token = parts[1]
                try:
                    r = requests.get(f"{API_BASE}/bind_info?access_token={token}", timeout=20)
                    send(chat_id, str(r.json()))
                except Exception as e:
                    send(chat_id, f"Error: {str(e)}")

        return "ok"

    except Exception as e:
        return str(e), 500


def send(chat_id, text):
    requests.post(TELEGRAM_API, json={
        "chat_id": chat_id,
        "text": text
    })
