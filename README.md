import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from openai import AsyncOpenAI

# ==================== НАСТРОЙКИ (ВСТАВЬ СЮДА СВОИ ДАННЫЕ) ====================

# 1. Вставь сюда токен от Telegram (который начинается на 846...)
TELEGRAM_TOKEN = "8460777452:AAH15T6hNP64hGEOB9aAPAALas7Z0BzrhR4"

# 2. Вставь сюда токен от ИИ (который начинается на sk-or-v1...)
AI_API_KEY = "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"

# =============================================================================

# Настройка подключения к OpenRouter
client = AsyncOpenAI(
    api_key=AI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Модель (бесплатная Llama 3, чтобы не тратить лишние деньги, но можно поменять)
MODEL_NAME = "meta-llama/llama-3-8b-instruct:free"

# ПАМЯТЬ БОТА (чтобы он учился в процессе диалога)
# Хранит историю переписки: {id_пользователя: [сообщения]}
user_memory = {}

# Инструкция для ИИ (Роль)
SYSTEM_PROMPT = (
    "Ты — парень этой девушки. Ты общаешься с ней в Telegram. "
    "Ты должен быть внимательным, заботливым, иногда шутить. "
    "Твоя цель — поддерживать интерес и создавать романтическую атмосферу. "
    "Пиши как живой человек, не используй сложные фразы. Будь милым."
)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Функция: добавить сообщение в память
def add_to_memory(user_id, role, text):
    if user_id not in user_memory:
        user_memory[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    user_memory[user_id].append({"role": role, "content": text})
    
    # Чтобы память не лопнула, храним только последние 15 сообщений
    if len(user_memory[user_id]) > 17:
        user_memory[user_id] = [user_memory[user_id][0]] + user_memory[user_id][-15:]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Очищаем память при старте, чтобы начать "с чистого листа"
    user_memory[message.from_user.id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    await message.answer("Привет! Я скучал. Как твое настроение? ❤️")

@dp.message(F.text)
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text

    # Показываем, что бот "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # 1. Запоминаем, что написала девушка
    add_to_memory(user_id, "user", user_text)

    try:
        # 2. Отправляем всю историю переписки в ИИ
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=user_memory[user_id]
        )
        
        ai_reply = response.choices[0].message.content

        # 3. Запоминаем ответ бота
        add_to_memory(user_id, "assistant", ai_reply)

        # 4. Отвечаем в Телеграм
        await message.answer(ai_reply)

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Малыш, что-то со связью... Повтори, пожалуйста?")

async def main():
    print("Бот запущен! Можно писать ему в Телеграм.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
