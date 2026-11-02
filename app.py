import os
import threading
import telebot
from flask import Flask
from gigachat import GigaChat

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = '9104126627:AAF7nYOAppsjGRV7DDDtu2MTndISZ5M6bIU'
GIGACHAT_KEY = 'MDFhMTlkYjAtNGI4OC03ZWE4LWFkMmItYTU3MjEyODg2ZWVjOjFiNzRhZDAzLWVmN2UtNGM2OS04N2UyLTliZjJmOTQ4OWMwYg=='

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Инициализация GigaChat
giga = GigaChat(
    credentials=GIGACHAT_KEY,
    scope='GIGACHAT_API_PERS',
    verify_ssl_certs=False,
    model='GigaChat'
)

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
@app.route('/')
def index():
    return "AI Bot is running!"

@app.route('/health')
def health():
    return "OK"

# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я ИИ-бот на GigaChat. Напиши мне что-нибудь, и я отвечу.")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        response = giga.chat(message.text)
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        print(f"Ошибка GigaChat: {e}")
        bot.reply_to(message, "Произошла ошибка при обращении к ИИ. Попробуй позже.")

# --- ЗАПУСК ---
def run_bot():
    print("Бот запущен...")
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
