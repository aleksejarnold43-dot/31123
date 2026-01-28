import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

# Настройка ИИ
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# Новый адекватный стиль
STYLE = "Ты — крутой и позитивный бро. Отвечай на сленге, дружелюбно, используй только маленькие буквы. Помогай юзеру, но будь на стиле."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Прямой запрос без лишних настроек (для стабильности)
        prompt = f"{STYLE}\nЮзер спросил: {m.text}\nТвой ответ:"
        res = model.generate_content(prompt)
        
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "бро, чет мысль потерял, повтори еще раз")
            
    except Exception as e:
        # Если будет ошибка — ты увидишь её в логах Amvera
        print(f"ОШИБКА: {e}")
        bot.reply_to(m, "слушай, чет гугл меня подводит, ща исправлюсь")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ ЗАПУЩЕН В РЕЖИМЕ ПОЗИТИВНОГО БРО!")
    bot.infinity_polling()
