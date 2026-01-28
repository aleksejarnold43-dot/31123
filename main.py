import telebot
import requests
from urllib.parse import quote

# ТВОЙ ТОКЕН
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"

bot = telebot.TeleBot(TG_TOKEN)

STYLE = "Твое имя — Рыжий Гномик. Ты невероятно вежливый, добрый и грамотный. Ты отлично знаешь математику, русский язык, литературу и биологию. Твоя миссия — помогать с любовью. Если другу грустно, прояви сострадание. Если весело — шути и играй. Всегда придерживайся морали и отвечай только маленькими буквами, но очень тепло."
@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Готовим текст
        prompt = f"{STYLE}\nЮзер: {m.text}\nОтвет:"
        # Кодируем для ссылки
        url_text = quote(prompt)
        
        # Шлем запрос на Pollinations (ОН РАБОТАЕТ В РФ)
        # model=openai - обычно самая стабильная
        url = f"https://text.pollinations.ai/{url_text}?model=openai"
        
        response = requests.get(url, timeout=25)
        
        if response.status_code == 200:
            bot.reply_to(m, response.text.lower())
        else:
            bot.reply_to(m, "слышь, сервак перегружен")
            
    except Exception as e:
        # Если совсем беда, пишем в лог, а юзеру - заглушку
        print(f"Ошибка: {e}")
        bot.reply_to(m, "связь тупит, сек...")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
    except:
        pass
    print("БОТ ЗАПУЩЕН (ВЕРСИЯ ДЛЯ РФ)!")
    bot.infinity_polling()
