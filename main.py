import telebot
import requests
import json

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
OPENROUTER_KEY = "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"

bot = telebot.TeleBot(TG_TOKEN)

# Инструкция для ИИ
STYLE = "Ты — дерзкий пацан с района. Общайся на сленге, коротко, только маленькими буквами. Используй слова: слышь, че каво, ровно, базаришь."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Запрос к OpenRouter
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": STYLE},
                    {"role": "user", "content": m.text}
                ]
            })
        )
        
        data = response.json()
        
        # Проверяем, есть ли ответ в данных
        if 'choices' in data:
            reply = data['choices'][0]['message']['content']
            bot.reply_to(m, reply.lower())
        else:
            print(f"Ошибка API: {data}")
            bot.reply_to(m, "слышь, чет я приуныл, повтори еще раз")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        bot.reply_to(m, "косяк какой-то, тормози")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ НА OPENROUTER ЗАПУЩЕН!")
    bot.infinity_polling()
