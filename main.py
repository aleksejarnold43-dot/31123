import telebot
from g4f.client import Client

# ТОЛЬКО ТВОЙ ТОКЕН ТЕЛЕГИ
TG_TOKEN = "7950976776:AAFXfDfpf3F1r0aDuhe2iuL0rfwyB5fTFh4"

bot = telebot.TeleBot(TG_TOKEN)
client = Client()

STYLE = "ты дерзкий пацан с района, общайся на сленге, коротко, только маленькими буквами. используй слова: слышь, базаришь, ровно."

@bot.message_handler(func=lambda m: True)
def echo(m):
    try:
        # Запрос к ИИ без
