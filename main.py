import telebot
import requests
import json

TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
OPENROUTER_KEY = "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"

bot = telebot.TeleBot(TG_TOKEN)

STYLE = "ты дерзкий пацан с района, общайся на сленге, коротко, только маленькими буквами."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            data=json.dumps({
                "model": "google/gemma-7b-it:free", # Поменял модель на более свободную
                "messages": [
                    {"role": "system", "content": STYLE},
                    {"role": "user", "content": m.text}
                ]
            })
        )
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            text = result['choices'][0]['message']['content']
            bot.reply_to(m, text.lower())
        else:
            # Если модель занята, бот скажет почему
            error_info = result.get('error', {}).get('message', 'неизвестная беда')
            bot.reply_to(m, f"тормози, сервак пишет: {error_info[:50]}")

    except Exception as e:
        bot.reply_to(m, "косяк с инетом, попробуй еще раз")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
