import requests
from flask import Flask, request, jsonify
from telegram import Bot, Update

app = Flask(__name__)

BOT_TOKEN = "8707631665:AAF_wbQXcwWfCSz6ySTwbcxizzSQEMnZoC8"
API_BASE = "https://email-checke38.vercel.app"

bot = Bot(BOT_TOKEN)

# ==============================
# API ROUTES
# ==============================

@app.route("/bind_info", methods=["GET"])
def bind_info():
    access_token = request.args.get("access_token")

    if not access_token:
        return jsonify({"status": "error", "error": "access_token required"}), 400

    try:
        r = requests.get(f"{API_BASE}/bind_info?access_token={access_token}")
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# ==============================
# TELEGRAM WEBHOOK
# ==============================

@app.route("/", methods=["GET"])
def home():
    return "Bot Running", 200


@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat_id
            text = update.message.text or ""

            if text.startswith("/start"):
                bot.send_message(
                    chat_id=chat_id,
                    text="🤖 Bot Active\n\nUse:\n/bind ACCESS_TOKEN\n/health"
                )

            elif text.startswith("/health"):
                bot.send_message(chat_id=chat_id, text="🟢 Server Running")

            elif text.startswith("/bind"):
                parts = text.split(" ")
                if len(parts) < 2:
                    bot.send_message(chat_id=chat_id, text="Usage:\n/bind ACCESS_TOKEN")
                else:
                    token = parts[1]
                    r = requests.get(f"{API_BASE}/bind_info?access_token={token}")
                    bot.send_message(chat_id=chat_id, text=str(r.json()))

        return "ok"

    except Exception as e:
        return str(e), 500
