import os
from flask import Flask, request
import telebot

# Получаем токен и адрес вебхука из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Привет! Это бот Usta KG. Напиши, какую услугу тебе нужно найти.")

# Обработка всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.strip()
    username = message.from_user.username or "Без username"
    full_message = f"📩 Новая заявка от @{username}:\n\n{text}"
    
    # Отправляем заявку админу
    bot.send_message('@alfaperson42', full_message)
    
    # Подтверждение пользователю
    bot.send_message(message.chat.id, "✅ Ваша заявка отправлена мастерам. Мы свяжемся с вами в ближайшее время.")

# Flask route для приёма обновлений от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200

# Установка вебхука при запуске
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

# Запуск Flask-сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

