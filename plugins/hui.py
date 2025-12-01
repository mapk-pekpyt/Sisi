import random
import datetime
from main import bot, db_execute, get_display_name

def change_hui(chat_id, user_id):
    today = datetime.date.today().isoformat()
    chat, user = str(chat_id), str(user_id)
    row = db_execute("SELECT size_cm,last_date FROM hui WHERE chat_id=? AND user_id=?", (chat,user), fetch=True)
    size = row[0]['size_cm'] if row else 0
    last = row[0]['last_date'] if row else None
    if last == today: return 0, size
    delta = random.randint(-10,10)
    if size + delta < 0: delta = -size
    new_size = size + delta
    db_execute("INSERT OR REPLACE INTO hui(chat_id,user_id,size_cm,last_date) VALUES (?,?,?,?)", (chat,user,new_size,today))
    return delta, new_size

@bot.message_handler(commands=['hui'])
def cmd_hui(m):
    chat_id, user_id = m.chat.id, m.from_user.id
    name = get_display_name(chat_id, user_id)
    delta, new_size = change_hui(chat_id, user_id)
    if delta == 0:
        bot.reply_to(m, f"Ой, а ты уже пробовал сегодня 😅\nТекущий хуй — <b>{new_size} см</b> 🍌")
    else:
        sign = f"{delta:+d}"
        bot.reply_to(m, f"🍌 {name}, твой хуй вырос на <b>{sign} см</b>, теперь — <b>{new_size} см</b> 🍌")