import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from fastapi import FastAPI, Request
import uvicorn
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.getenv("BOT_TOKEN")
DOMAIN = "https://usta-kgbot-1.onrender.com"  # URL из Render

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

class Order(StatesGroup):
    waiting_for_category = State()
    waiting_for_description = State()
    waiting_for_location = State()

categories = ["Сантехник", "Электрик", "Грузчик", "Мастер на час", "Уборка", "Другое"]

@dp.message(commands=["start"])
async def start_handler(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    for cat in categories:
        keyboard.add(InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}"))
    await message.answer("Привет! Выбери категорию услуги:", reply_markup=keyboard)
    await state.set_state(Order.waiting_for_category)

@dp.callback_query(lambda c: c.data.startswith("cat_"))
async def category_selected(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data[4:]
    await state.update_data(category=category)
    await callback_query.message.answer("Опиши, что нужно сделать:")
    await state.set_state(Order.waiting_for_description)
    await callback_query.answer()

@dp.message(Order.waiting_for_description)
async def description_handler(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Отправь локацию, где нужно выполнить услугу:")
    await state.set_state(Order.waiting_for_location)

@dp.message(Order.waiting_for_location)
async def location_handler(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer("Пожалуйста, отправь локацию с помощью кнопки 📍.")
        return

    data = await state.get_data()
    category = data["category"]
    description = data["description"]
    lat = message.location.latitude
    lon = message.location.longitude

    order_text = (
        f"📥 <b>Новая заявка</b>\n\n"
        f"<b>Категория:</b> {category}\n"
        f"<b>Описание:</b> {description}\n"
        f"<b>Локация:</b> https://maps.google.com/?q={lat},{lon}"
    )

    await bot.send_message(chat_id="@alfaperson42", text=order_text)
    await message.answer("Спасибо! Заявка отправлена ✅")
    await state.clear()

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{DOMAIN}/webhook"
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
