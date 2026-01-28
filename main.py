import telebot
import google.generativeai as genai

TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyAOGk2YU7z-c9maf5gHlcY8QLjuUPY0nuQ"

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# МАКСИМАЛЬНО ПРОСТОЙ СТИЛЬ ДЛЯ ПРОВЕРКИ
STYLE = "Ты — обычный ассистент. Отвечай коротко."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Прямой запрос без настроек безопасности (по умолчанию)
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        if res.text:
            bot.reply_to(m, res.text)
        else:
            bot.reply_to(m, "ИИ вернул пустой ответ")
    except Exception as e:
        # Если снова ошибка - пришлет её текст в телегу
        bot.reply_to(m, f"Ошибка ключа: {str(e)[:50]}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
