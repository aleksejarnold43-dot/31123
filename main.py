import telebot
import requests
from urllib.parse import quote

# ТВОЙ ТОКЕН
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"

bot = telebot.TeleBot(TG_TOKEN)

STYLE = "ты — дерзкий тип с района. общайся максимально нагло, используй жесткий сленг, подколы и сарказм. отвечай коротко, только маленькими буквами. не сопливь, будь резким, как пуля,  не сильные маты."

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
