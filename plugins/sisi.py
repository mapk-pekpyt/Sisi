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

def change_boobs(chat_id, user_id):
    today = datetime.date.today().isoformat()
    row = db_execute("SELECT size,last_date FROM boobs WHERE chat_id=? AND user_id=?", (str(chat_id), str(user_id)), fetch=True)
    if row:
        size = row[0]["size"]
        last = row[0]["last_date"]
    else:
        size = 0
        last = None

    if last == today:
        return 0, size

    delta = random.randint(-10, 10)
    if size + delta < 0:
        delta = -size
    new_size = size + delta
    db_execute("INSERT OR REPLACE INTO boobs(chat_id,user_id,size,last_date) VALUES (?,?,?,?)",
               (str(chat_id), str(user_id), new_size, today))
    return delta, new_size

def setup(bot):
    @bot.message_handler(commands=['sisi'])
    def cmd_sisi(m):
        chat_id = m.chat.id
        user_id = m.from_user.id
        delta, new_size = change_boobs(chat_id, user_id)
        if delta == 0:
            bot.reply_to(m, f"Ой, а ты уже пробовал сегодня 😅\nТвой текущий размер груди — <b>{new_size}</b> 🍒")
        else:
            sign = f"{delta:+d}"
            bot.reply_to(m, f"🍒 Твой размер груди вырос на <b>{sign}</b>, теперь твой размер груди — <b>{new_size}</b> 🍒")