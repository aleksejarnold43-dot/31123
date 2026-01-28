import telebot
import google.generativeai as genai

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
GOOGLE_KEY = "AIzaSyAOGk2YU7z-c9maf5gHlcY8QLjuUPY0nuQ"

genai.configure(api_key=GOOGLE_KEY)
bot = telebot.TeleBot(TG_TOKEN)

# ФУНКЦИЯ АВТОПОДБОРА МОДЕЛИ
def find_working_model():
    try:
        # Получаем список всех моделей, доступных твоему ключу
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5' in m.name or 'gemini-pro' in m.name:
                    print(f"Найдена рабочая модель: {m.name}")
                    return genai.GenerativeModel(m.name)
    except Exception as e:
        print(f"Ошибка при поиске моделей: {e}")
    return None

model = find_working_model()

STYLE = "ты простой пацан с района, общайся на сленге, коротко, только маленькими буквами."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        if not model:
            bot.reply_to(m, "слышь, ключи не пашут или моделей нет")
            return
            
        res = model.generate_content(f"{STYLE}\nЮзер: {m.text}")
        bot.reply_to(m, res.text.lower())
    except Exception as e:
        bot.reply_to(m, f"косяк: {str(e)[:50]}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ ЗАПУЩЕН!")
    bot.infinity_polling()
