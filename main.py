import telebot
from g4f.client import Client

# ТВОЙ ТОКЕН
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"

bot = telebot.TeleBot(TG_TOKEN)
client = Client()

STYLE = "ты дерзкий пацан с района, общайся на сленге, коротко, только маленькими буквами."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # ВАЖНО: Все строки ниже должны иметь отступ (4 пробела)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{STYLE}\nЮзер: {m.text}"}],
        )
        reply = response.choices[0].message.content
        bot.reply_to(m, reply.lower())
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(m, "слышь, чето связь на районе тухлая")

if __name__ == "__main__":
    bot.remove_webhook()
    print("БОТ ЗАПУЩЕН!")
    bot.infinity_polling()
