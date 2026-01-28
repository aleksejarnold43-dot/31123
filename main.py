import telebot
import requests
from urllib.parse import quote

# ТВОЙ ТОКЕН ТЕЛЕГИ (ЕДИНСТВЕННОЕ, ЧТО НУЖНО)
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"

bot = telebot.TeleBot(TG_TOKEN)

# Стиль пацана
STYLE = "ты дерзкий пацан с района. отвечай на сленге, коротко, грубовато, только маленькими буквами. не используй умные слова."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # 1. Готовим текст запроса
        prompt = f"{STYLE}\nЮзер пишет: {m.text}\nТвой ответ:"
        
        # 2. Кодируем текст для ссылки (чтобы пробелы стали %20 и т.д.)
        url_prompt = quote(prompt)
        
        # 3. ОТПРАВЛЯЕМ ЗАПРОС НА БЕСПЛАТНЫЙ СЕРВЕР (БЕЗ КЛЮЧЕЙ!)
        # Используем модель OpenAI через открытый шлюз
        response = requests.get(f"https://text.pollinations.ai/{url_prompt}?model=openai")
        
        # 4. Проверяем ответ
        if response.status_code == 200:
            bot.reply_to(m, response.text.lower())
        else:
            bot.reply_to(m, "слышь, сервак перегружен, пробуй позже")
            
    except Exception as e:
        bot.reply_to(m, f"какая-то дичь: {e}")

if __name__ == "__main__":
    # Убираем старые ошибки
    bot.remove_webhook()
    print("БОТ ЗАПУЩЕН БЕЗ КЛЮЧЕЙ!")
    bot.infinity_polling()
