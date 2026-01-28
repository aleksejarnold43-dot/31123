import telebot
import requests
import json
import time

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
OR_KEY = "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"

bot = telebot.TeleBot(TG_TOKEN)

# Стиль пацана
STYLE = "ты дерзкий тип. отвечай на сленге, грубовато, но по делу. используй только маленькие буквы."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Заголовки ОБЯЗАТЕЛЬНЫ для OpenRouter
        headers = {
            "Authorization": f"Bearer {OR_KEY}",
            "HTTP-Referer": "https://amvera.ru",
            "X-Title": "BroBot",
            "Content-Type": "application/json"
        }
        
        # Пробуем самую простую модель
        data = {
            "model": "google/gemma-7b-it:free",
            "messages": [
                {"role": "system", "content": STYLE},
                {"role": "user", "content": m.text}
            ]
        }

        # Отправляем запрос
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=30
        )
        
        # Читаем ответ
        if response.status_code == 200:
            json_resp = response.json()
            if 'choices' in json_resp:
                reply = json_resp['choices'][0]['message']['content']
                bot.reply_to(m, reply.lower())
            else:
                bot.reply_to(m, "слышь, пустоту прислали")
        else:
            # Если ошибка - выводим код ошибки прямо в чат
            error_text = response.text
            bot.reply_to(m, f"Сервер OpenRouter ругается: {response.status_code}\n{error_text[:100]}")

    except Exception as e:
        bot.reply_to(m, f"Ошибка кода: {e}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        bot.remove_webhook()
    except:
        pass
    print("БОТ ЗАПУЩЕН! ЖДУ СООБЩЕНИЙ")
    bot.infinity_polling()
