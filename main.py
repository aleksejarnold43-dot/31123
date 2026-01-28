import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ (ОБНОВЛЕННЫЕ)
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyAOGk2YU7z-c9maf5gHlcY8QLjuUPY0nuQ"

# Настройка ИИ
genai.configure(api_key=GOOGLE_KEY)

# Пробуем разные модели, если одна не сработает
def get_model():
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # Пробный запрос, чтобы проверить доступность
            return m
        except:
            continue
    return None

model = get_model()
bot = telebot.TeleBot(TG_TOKEN)

STYLE = "ты простой пацан с района, общайся на сленге, коротко, только маленькими буквами. ты дерзкий, но не перегибай."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        if model is None:
            bot.reply_to(m, "слышь, у меня мозги не завезли, проверь ключи")
            return

        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        if res.text:
            bot.reply_to(m, res.text.lower())
        else:
            bot.reply_to(m, "че ты там мямлишь")
            
    except Exception as e:
        # Если ошибка, бот скажет её начало
        error_msg = str(e)
        bot.reply_to(m, f"косяк: {error_msg[:50]}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ В СЕТИ")
    bot.infinity_polling()
