import os
import sqlite3
import telebot
import importlib

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Путь к базе
DB = os.path.join(os.path.dirname(__file__), "boobs.db")

# === Функции работы с БД ===
def db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def db_execute(query, params=(), fetch=False):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

# === Создание таблиц (обязательно перед загрузкой плагинов) ===
db_execute("""CREATE TABLE IF NOT EXISTS boobs (
    chat_id TEXT,
    user_id TEXT,
    size INTEGER,
    last_date TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")
db_execute("""CREATE TABLE IF NOT EXISTS klitor (
    chat_id TEXT,
    user_id TEXT,
    size_mm INTEGER,
    last_date TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")
db_execute("""CREATE TABLE IF NOT EXISTS hui (
    chat_id TEXT,
    user_id TEXT,
    size_cm INTEGER,
    last_date TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")
db_execute("""CREATE TABLE IF NOT EXISTS whoami (
    chat_id TEXT,
    user_id TEXT,
    choice TEXT,
    date TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")
db_execute("""CREATE TABLE IF NOT EXISTS names (
    chat_id TEXT,
    user_id TEXT,
    display_name TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")
db_execute("""CREATE TABLE IF NOT EXISTS birthdays (
    chat_id TEXT,
    user_id TEXT,
    date TEXT,
    PRIMARY KEY(chat_id, user_id)
)""")

# === Динамическая загрузка плагинов ===
PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "plugins")
for filename in os.listdir(PLUGINS_DIR):
    if filename.endswith(".py") and not filename.startswith("__"):
        modulename = filename[:-3]
        importlib.import_module(f"plugins.{modulename}")

# === Запуск бота ===
if __name__=="__main__":
    bot.infinity_polling(skip_pending=True)