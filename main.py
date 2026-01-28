import telebot
import requests

# ТВОИ КЛЮЧИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"
# Используем бесплатный API Hugging Face (модель Mistral)
API_URL = "https://api-inference.huggingface.co/models/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": "Bearer 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"} # Временный ключ для теста

bot = telebot.TeleBot(TG_TOKEN)

STYLE = "Ты - дерзкий пацан. Отвечай очень коротко и на сленге."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        payload = {"inputs": f"<s>[INST] {STYLE} Юзер: {m.text} [/INST]"}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        output = response.json()
        
        # Вытаскиваем текст ответа
        if isinstance(output, list) and 'generated_text' in output[0]:
            full_text = output[0]['generated_text']
            reply = full_text.split("[/INST]")[-1].strip()
            bot.reply_to(m, reply.lower())
        else:
            bot.reply_to(m, "слышь, чето я задумался, черкани еще раз")
            print(f"Ответ сервера: {output}")

    except Exception as e:
        bot.reply_to(m, "косяк, база не отвечает")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ ПЕРЕЗАПУЩЕН НА НОВОМ ДВИЖКЕ!")
    bot.infinity_polling()
