import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ (НЕ ТРОГАЙ ИХ, ОНИ РАБОЧИЕ)
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

# Настройка ИИ
genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# Стиль: "хулиган", но без слов, которые блочит Гугл
STYLE = "Ты — пацан с района. Говоришь на сленге, дерзко, только маленькими буквами. Ты не любишь лишних вопросов."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Пытаемся получить ответ
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "че ты там мямлишь, не понял нихуя")
            
    except Exception as e:
        # Если Гугл заблочил - бот ответит сам в своем стиле
        print(f"Ошибка ИИ: {e}")
        bot.reply_to(m, "слышь, чет меня переклинило, давай по новой")

if __name__ == "__main__":
    print("Удаляем старые вебхуки...")
    bot.remove_webhook() # Это лечит ошибку 409
    print("БОТ ЗАПУЩЕН!")
    bot.infinity_polling()
