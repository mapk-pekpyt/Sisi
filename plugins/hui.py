import random, datetime, sqlite3

DB = "boobs.db"

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

def change_hui(chat_id, user_id):
    today = datetime.date.today().isoformat()
    row = db_execute("SELECT size_cm,last_date FROM hui WHERE chat_id=? AND user_id=?", (str(chat_id), str(user_id)), fetch=True)
    if row:
        size = row[0]["size_cm"]
        last = row[0]["last_date"]
    else:
        size = 0
        last = None

    if last == today:
        return 0, size

    delta = random.randint(-10, 10)  # см
    if size + delta < 0:
        delta = -size
    new_size = size + delta
    db_execute("INSERT OR REPLACE INTO hui(chat_id,user_id,size_cm,last_date) VALUES (?,?,?,?)",
               (str(chat_id), str(user_id), new_size, today))
    return delta, new_size

def setup(bot):
    @bot.message_handler(commands=['hui'])
    def cmd_hui(m):
        chat_id = m.chat.id
        user_id = m.from_user.id
        delta, new_size = change_hui(chat_id, user_id)
        if delta == 0:
            bot.reply_to(m, f"Ой, уже сегодня 😅\nТекущий размер хуя — <b>{new_size} см</b> 🍒")
        else:
            sign = f"{delta:+d}"
            bot.reply_to(m, f"🍒 Размер хуя изменился на <b>{sign} см</b>, теперь он — <b>{new_size} см</b> 🍒")