import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

# Настройка ИИ 1.5 Flash
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# Инструкция без триггеров для фильтров
STYLE = "Ты — позитивный бро. Общайся на сленге, коротко, используй только маленькие буквы. Будь на чилле."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Просим ИИ ответить на сообщение
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "бро, чет я задумался, черкани еще раз")
            
    except Exception as e:
        # Если ИИ все равно блочит — бот просто ответит сам без мата
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(m, "слушай, чет связь барахлит, давай позже")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ В СЕТИ!")
    bot.infinity_polling()
