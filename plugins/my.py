from main import bot, db_execute, get_display_name

@bot.message_handler(commands=['my'])
def cmd_my(m):
    chat_id, user_id = str(m.chat.id), str(m.from_user.id)
    boobs = db_execute("SELECT size FROM boobs WHERE chat_id=? AND user_id=?", (chat_id,user_id), fetch=True)
    klitor = db_execute("SELECT size_mm FROM klitor WHERE chat_id=? AND user_id=?", (chat_id,user_id), fetch=True)
    hui = db_execute("SELECT size_cm FROM hui WHERE chat_id=? AND user_id=?", (chat_id,user_id), fetch=True)
    bot.reply_to(m,
                 f"✨ {get_display_name(m.chat.id, m.from_user.id)}, ваши размеры:\n"
                 f"Грудь: <b>{boobs[0]['size'] if boobs else 0}</b> 🍒\n"
                 f"Клитор: <b>{klitor[0]['size_mm'] if klitor else 0} мм</b> 🍆\n"
                 f"Хуй: <b>{hui[0]['size_cm'] if hui else 0} см</b> 🍌")