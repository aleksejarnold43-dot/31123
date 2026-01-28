import telebot
import requests
import json

# ТВОИ ДАННЫЕ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
OR_KEY = "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"

bot = telebot.TeleBot(TG_TOKEN)

STYLE = "ты дерзкий пацан, общайся на сленге, коротко, только маленькими буквами. хами по красоте."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Прямой запрос к OpenRouter с жесткими настройками
        headers = {
            "Authorization": f"Bearer {OR_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://amvera.ru", # Это важно для OpenRouter
        }
        
        data = {
            "model": "google/gemma-7b-it:free",
            "messages": [{"role": "user", "content": f"{STYLE}\nЮзер: {m.text}"}]
        }

        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data), timeout=20)
        
        result = res.json()
        
        if 'choices' in result:
            answer = result['choices'][0]['message']['content']
            bot.reply_to(m, answer.lower())
        else:
            # Если ИИ тупит, выводим причину в лог и юзеру коротко
            err = result.get('error', {}).get('message', 'база лежит')
            bot.reply_to(m, f"слышь, тут косяк: {err[:30]}")
            
    except Exception as e:
        bot.reply_to(m, "тормози, сеть лагает")

if __name__ == "__main__":
    bot.remove_webhook()
    print("ВСЁ, БОТ ПОГНАЛ!")
    bot.infinity_polling()
