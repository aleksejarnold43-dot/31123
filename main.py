import telebot
import google.generativeai as genai

TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBn_JuyBetYxrHvxHMkOHEVXQBbavNdQeI"

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TG_TOKEN)

# Убрали слова "мат", "грубо", "посылай". Заменили на "плохой парень".
STYLE = "Ты — очень плохой парень с района. Говоришь на сленге, дерзко, используешь только маленькие буквы. Короткие ответы."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Добавляем примеры, чтобы ИИ понял стиль без запрещенных слов
        prompt = f"{STYLE}\nПример: слышь, ты че тут забыл?\nЮзер: {m.text}\nТвой ответ:"
        
        # Настройки безопасности прямо в запросе
        res = model.generate_content(
            prompt,
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )
        
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "че ты там мямлишь")
            
    except Exception as e:
        # Если всё равно ошибка, выведи её в логи Amvera!
        print(f"ОШИБКА: {e}")
        bot.reply_to(m, "слышь чет я тебя не понял")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
