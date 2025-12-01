from main import bot, db_execute, get_display_name

def top_text(table, chat_id, unit):
    key = "size" if table=="boobs" else ("size_mm" if table=="klitor" else "size_cm")
    rows = db_execute(f"SELECT user_id,{key} AS s FROM {table} WHERE chat_id=? ORDER BY s DESC LIMIT 10", (str(chat_id),), fetch=True)
    if not rows:
        return "Пусто 😅"
    text = f"🏆 ТОП {table}:\n\n"
    for i,r in enumerate(rows,start=1):
        name = get_display_name(chat_id,r['user_id'])
        text += f"{i}. {name} — {r['s']} {unit}\n"
    return text

@bot.message_handler(commands=['topsisi'])
def cmd_topsisi(m):
    bot.reply_to(m, top_text("boobs", m.chat.id, "🍒"))

@bot.message_handler(commands=['topklitor'])
def cmd_topklitor(m):
    bot.reply_to(m, top_text("klitor", m.chat.id, "мм 🍆"))

@bot.message_handler(commands=['tophui'])
def cmd_tophui(m):
    bot.reply_to(m, top_text("hui", m.chat.id, "см 🍌"))