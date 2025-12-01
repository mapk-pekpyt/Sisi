import os
import importlib
import telebot
import sqlite3
import datetime
import random
import re

# ====== Настройки ======
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DB = "boobs.db"
PHOTO_DIR = "photos"
ADMIN_USERNAME = "Sugar_Daddy_rip"
DONATE_PRICE = 10

# ====== База ======
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

def init_db():
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

init_db()

# ====== Общие функции ======
def get_stored_name(chat_id, user_id):
    row = db_execute("SELECT display_name FROM names WHERE chat_id=? AND user_id=?", (str(chat_id), str(user_id)), fetch=True)
    return row[0]["display_name"] if row else None

def get_user_name_fallback(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        user = member.user
        if getattr(user, "last_name", None):
            return f"{user.first_name} {user.last_name}"
        return user.first_name or "Пользователь"
    except Exception:
        return "Пользователь"

def get_display_name(chat_id, user_id):
    return get_stored_name(chat_id, user_id) or get_user_name_fallback(chat_id, user_id)

def change_size(table, chat_id, user_id, delta_range=(-10,10)):
    today = datetime.date.today().isoformat()
    chat, user = str(chat_id), str(user_id)
    row = db_execute(f"SELECT * FROM {table} WHERE chat_id=? AND user_id=?", (chat, user), fetch=True)
    if row:
        last = row[0]["last_date"]
        size_key = "size" if table=="boobs" else ("size_mm" if table=="klitor" else "size_cm")
        size = row[0][size_key]
    else:
        last = None
        size = 0
    if last == today:
        return 0, size
    delta = random.randint(delta_range[0], delta_range[1])
    if size + delta < 0:
        delta = -size
    new_size = size + delta
    size_key = "size" if table=="boobs" else ("size_mm" if table=="klitor" else "size_cm")
    db_execute(f"INSERT OR REPLACE INTO {table}(chat_id,user_id,{size_key},last_date) VALUES (?,?,?,?)",
               (chat, user, new_size, today))
    return delta, new_size

def whoami(chat_id, user_id):
    today = datetime.date.today().isoformat()
    chat, user = str(chat_id), str(user_id)
    row = db_execute("SELECT choice,date FROM whoami WHERE chat_id=? AND user_id=?", (chat, user), fetch=True)
    if row and row[0]["date"] == today:
        return row[0]["choice"]
    choice = random.choice(["ты лох 😏", "удивительно, но сегодня ты не лох 🎉"])
    db_execute("INSERT OR REPLACE INTO whoami(chat_id,user_id,choice,date) VALUES (?,?,?,?)",
               (chat, user, choice, today))
    return choice

# ====== Загрузка плагинов ======
PLUGIN_FOLDER = "plugins"
for f in os.listdir(PLUGIN_FOLDER):
    if f.endswith(".py") and not f.startswith("__"):
        importlib.import_module(f"{PLUGIN_FOLDER}.{f[:-3]}")

# ====== Запуск ======
if __name__=="__main__":
    bot.infinity_polling(skip_pending=True)