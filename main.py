from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = "7901632898:AAFF5UShYE8-cEC71ABnJX9gC_zpClwBtZQ"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Главная точка для Telegram Webhook
@app.route('/', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot=bot, update_queue=None)
    
    # Хендлер команды /start
    dispatcher.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("Привет! Я бот Usta KG.")))
    
    dispatcher.process_update(update)
    return "ok"

# Проверка, что бот жив
@app.route('/', methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
