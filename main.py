import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

import asyncio

TOKEN = "7901632898:AAFF5UShYE8-cEC71ABnJX9gC_zpClwBtZQ"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это бот Usta KG. Чем могу помочь?")

application.add_handler(CommandHandler("start", start))

# --- Flask webhook ---
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# --- Проверка работы сайта ---
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(port=5000)
