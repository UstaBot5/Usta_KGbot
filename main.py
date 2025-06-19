from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text('Добро пожаловать в Usta KG!')

updater = Updater(7901632898:AAFF5UShYE8-cEC71ABnJX9gC_zpClwBtZQ, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()
add working bot files
