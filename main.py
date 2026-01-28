import telebot
import google.generativeai as genai

TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

genai.configure(api_key=GOOGLE_KEY)
# Настраиваем ИИ так, чтобы он не блокировал грубость
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)
bot = telebot.TeleBot(TG_TOKEN)

# Чуть менее "триггерный" промпт для фильтров
STYLE = "Ты — очень грубый и дерзкий уличный пацан. Отвечай без цензуры, коротко, на сленге, только маленькими буквами. Можешь хамить."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "че ты там мычишь")
    except Exception as e:
        # Если даже так блок — выводим ошибку в логи, чтобы понять причину
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(m, "слышь чето меня кроет повтори позже")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
