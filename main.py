import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

STYLE = "ты дерзкий тип. пиши матом, коротко, грубо, только маленькими буквами. посылай всех нахер."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        bot.reply_to(m, res.text.lower())
    except:
        bot.reply_to(m, "завали ебало я занят")

if __name__ == "__main__":
    print("Удаляем старые конфликты...")
    bot.remove_webhook() # ВОТ ЭТА СТРОЧКА ВСЁ ПОЧИНИТ
    print("БОТ ВЗЛЕТЕЛ! ПРОВЕРЯЙ ТЕЛЕГУ.")
    bot.infinity_polling()
