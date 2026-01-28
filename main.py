import telebot
import google.generativeai as genai

TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# Убираем все "опасные" слова из инструкции
STYLE = "Ты — простой пацан с района, общаешься на расслабленном сленге, только маленькими буквами. Ты дружелюбный, но дерзкий."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Пытаемся получить ответ с минимальными ограничениями
        response = model.generate_content(
            f"{STYLE}\nЮзер: {m.text}",
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            }
        )
        
        if response.text:
            bot.reply_to(m, response.text.lower())
        else:
            bot.reply_to(m, "бро, чет я подвис, давай еще раз")
            
    except Exception as e:
        # Если ИИ всё равно блочит, бот ответит просто эхом, чтобы мы знали, что он жив
        bot.reply_to(m, f"я тебя слышу, ты сказал: {m.text}. но иишка чет тупит.")
        print(f"Ошибка ИИ: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
