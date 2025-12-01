import os
import telebot
from plugins import sisi, klitor, hui

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Подключаем плагины
sisi.setup(bot)
klitor.setup(bot)
hui.setup(bot)

print("Бот запущен!")

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)