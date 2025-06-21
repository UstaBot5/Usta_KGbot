from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

import os

TOKEN = os.environ.get("BOT_TOKEN")  # Убедись, что переменная окружения BOT_TOKEN установлена на Render

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot=bot, update_queue=None)
    # здесь добавь хендлеры
    return "ok"

@app.route('/', methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
