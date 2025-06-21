from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

# --- ВСТАВЛЕН ТВОЙ ТОКЕН ---
TOKEN = "7901632898:AAFF5UShYE8-cEC71ABnJX9gC_zpClwBtZQ"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# --- Создаем диспетчер один раз ---
dispatcher = Dispatcher(bot=bot, update_queue=None)

# --- Хендлер для команды /start ---
def start(update: Update, context):
    update.message.reply_text("Привет! Это бот Usta KG. Чем могу помочь?")

dispatcher.add_handler(CommandHandler("start", start))

# --- Webhook обработчик ---
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# --- Проверка доступности ---
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
