from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

TOKEN = os.getenv("BOT_TOKEN")  # Render автоматически подставляет переменные окружения
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://usta-kgbot.onrender.com/webhook

bot = Bot(token=TOKEN)
app = Flask(__name__)

# === Telegram bot setup ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ассаламу алейкум! Выберите категорию услуги:")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Спасибо, ваша заявка принята! Мы скоро свяжемся с вами.")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# === Flask routes ===
@app.route("/", methods=["GET"])
def index():
    return "Usta KG бот работает!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        await application.update_queue.put(update)
    return "ok"

# === Webhook setup (один раз при старте) ===
@app.before_first_request
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

# === Flask run for Render ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
