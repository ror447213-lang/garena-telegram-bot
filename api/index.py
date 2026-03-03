import requests
from flask import Flask, request

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
            send(chat_id,
                 "🤖 *Garena Bind Info Bot*\n\n"
                 "Use commands:\n"
                 "• /bind ACCESS_TOKEN\n"
                 "• /health",
                 markdown=True)

        elif text.startswith("/health"):
            send(chat_id, "🟢 Server Running 24/7")

        elif text.startswith("/bind"):
            parts = text.split(" ")

            if len(parts) < 2:
                send(chat_id, "Usage:\n/bind ACCESS_TOKEN")
            else:
                token = parts[1]

                try:
                    r = requests.get(
                        f"{API_BASE}/bind_info?access_token={token}",
                        timeout=20
                    )
                    data = r.json()

                    if data.get("status") == "success":
                        current = data["data"].get("current_email") or "None"
                        pending = data["data"].get("pending_email") or "None"
                        summary = data.get("summary", "No summary")

                        status_text = "Confirmed" if current != "None" else "Not Set"

                        reply = (
                            f"📧 *Current Email*\n{current}\n\n"
                            f"⏳ *Pending Email*\n{pending}\n\n"
                            f"✅ *Status*\n{status_text}\n\n"
                            f"📝 *Summary*\n{summary}"
                        )

                        send(chat_id, reply, markdown=True)

                    else:
                        send(chat_id, "❌ Failed to fetch data")

                except Exception as e:
                    send(chat_id, f"❌ Error:\n{str(e)}")

        return "ok"

    except Exception as e:
        return str(e), 500


def send(chat_id, text, markdown=False):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if markdown:
        payload["parse_mode"] = "Markdown"

    requests.post(TELEGRAM_API, json=payload)
