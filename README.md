import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from openai import AsyncOpenAI

# === БЕРЕМ КЛЮЧИ ИЗ СЕКРЕТОВ REPLIT (НЕ МЕНЯЙ ЭТО) ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")

if not TELEGRAM_TOKEN or not AI_API_KEY:
    print("ОШИБКА: Ты не добавил токены в Secrets (Замочек 🔒)!")
    exit()

# === НАСТРОЙКИ БОТА ===

# Настройка подключения к OpenRouter
client = AsyncOpenAI(
    api_key=AI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Модель (бесплатная Llama 3)
MODEL_NAME = "meta-llama/llama-3-8b-instruct:free"

# ПАМЯТЬ БОТА
user_memory = {}

# Роль бота
SYSTEM_PROMPT = (
    "Ты — парень этой девушки. Ты общаешься с ней в Telegram. "
    "Ты должен быть внимательным, заботливым, иногда шутить. "
    "Поддерживай диалог, спрашивай про её день. "
    "Отвечай кратко, но тепло, как живой человек."
)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Функция памяти
def add_to_memory(user_id, role, text):
    if user_id not in user_memory:
        user_memory[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    user_memory[user_id].append({"role": role, "content": text})
    # Храним последние 15 сообщений
    if len(user_memory[user_id]) > 17:
        user_memory[user_id] = [user_memory[user_id][0]] + user_memory[user_id][-15:]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_memory[message.from_user.id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    await message.answer("Привет, малыш! Я скучал. Как ты? ❤️")

@dp.message(F.text)
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text

    # Показываем статус "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    add_to_memory(user_id, "user", user_text)

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=user_memory[user_id]
        )
        
        ai_reply = response.choices[0].message.content
        add_to_memory(user_id, "assistant", ai_reply)
        await message.answer(ai_reply)

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Прости, задумался... Повтори?")

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Стоп")
