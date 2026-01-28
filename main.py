
import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyBaNWSUkW-SyrmBkmFkPCHqGCZYi7NwNvI"

# Настройка Гугла
genai.configure(api_key=GOOGLE_KEY)
bot = telebot.TeleBot(TG_TOKEN)

# Пытаемся взять самую быструю модель (Flash)
# Если она недоступна в регионе, переключимся на Pro
def get_model():
    for name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(name)
            return m
        except:
            continue
    return None

model = get_model()

# Стиль
STYLE = "ты дерзкий пацан, отвечай пулей, коротко и на сленге, только маленькими буквами."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        if not model:
            bot.reply_to(m, "слышь, гугл не дает модель, походу регион не тот")
            return

        # Настройки безопасности (чтобы не блокировал сленг)
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
            bot.reply_to(m, "че ты там промямлил?")
            
    except Exception as e:
        # Если закончились лимиты (ошибка 429)
        if "429" in str(e):
            bot.reply_to(m, "брат, тормози, дай отдышаться (лимиты)")
        else:
            print(f"Ошибка: {e}")
            bot.reply_to(m, "косяк какой-то, пробуй еще")

if __name__ == "__main__":
    bot.remove_webhook()
    print("СКОРОСТНОЙ БОТ ЗАПУЩЕН!")
    bot.infinity_polling()
