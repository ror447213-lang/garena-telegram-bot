import requests
from flask import Flask, request, jsonify
from telegram import Bot, Update

app = Flask(__name__)

# 🔐 YAHAN APNA TELEGRAM BOT TOKEN DALO
BOT_TOKEN = "8707631665:AAF_wbQXcwWfCSz6ySTwbcxizzSQEMnZoC8"

# Tumhara Garena API URL
API_BASE = "https://email-checke38.vercel.app"

bot = Bot(token=BOT_TOKEN)

# ==============================
# 🔹 GARINA API PART
# ==============================

@app.route('/bind_info', methods=['GET'])
def bind_info_endpoint():
    access_token = request.args.get('access_token')

    if not access_token:
        return jsonify({"status": "error", "error": "access_token required"}), 400

    r = requests.get(f"{API_BASE}/bind_info?access_token={access_token}")
    return jsonify(r.json()), r.status_code


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


# ==============================
# 🔹 TELEGRAM WEBHOOK (PUBLIC)
# ==============================

@app.route("/", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        text = update.message.text

        if text.startswith("/start"):
            bot.send_message(
                chat_id=update.message.chat_id,
                text="🤖 Welcome!\n\nUse:\n/bind ACCESS_TOKEN\n/health"
            )

        elif text.startswith("/health"):
            bot.send_message(
                chat_id=update.message.chat_id,
                text="🟢 Server Running 24/7"
            )

        elif text.startswith("/bind"):
            parts = text.split(" ")

            if len(parts) < 2:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Usage:\n/bind ACCESS_TOKEN"
                )
            else:
                token = parts[1]

                try:
                    r = requests.get(f"{API_BASE}/bind_info?access_token={token}")
                    data = r.json()

                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text=str(data)
                    )

                except Exception as e:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f"❌ Error:\n{str(e)}"
                    )

    return "ok"


@app.route("/", methods=["GET"])
def home():
    return "Public Telegram Bot Running", 200