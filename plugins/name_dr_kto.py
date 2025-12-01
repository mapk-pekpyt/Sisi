import re
from main import bot, db_execute, get_display_name, whoami

@bot.message_handler(commands=['name'])
def cmd_name(m):
    parts = m.text.split(maxsplit=1)
    if len(parts)<2:
        bot.reply_to(m,"Используй: /name ТвоёИмя")
        return
    db_execute("INSERT OR REPLACE INTO names(chat_id,user_id,display_name) VALUES (?,?,?)",
               (str(m.chat.id), str(m.from_user.id), parts[1].strip()))
    bot.reply_to(m,f"🎉 Ваше имя изменено на '{parts[1].strip()}'")

@bot.message_handler(commands=['dr'])
def cmd_dr(m):
    parts = m.text.split()
    chat_id, user_id = str(m.chat.id), str(m.from_user.id)
    if len(parts)==1:
        row = db_execute("SELECT date FROM birthdays WHERE chat_id=? AND user_id=?", (chat_id,user_id), fetch=True)
        bot.reply_to(m,f"🎂 Твой день рождения: {row[0]['date']}" if row else "🎂 Ты ещё не указал день рождения")
        return
    if parts[1].lower()=="all":
        rows = db_execute("SELECT user_id,date FROM birthdays WHERE chat_id=?", (chat_id,), fetch=True)
        if not rows:
            bot.reply_to(m,"🎂 Нет дней рождения 😅")
            return
        text = "🎂 Дни рождения чата:\n"
        for r in rows:
            name = get_display_name(chat_id,r['user_id'])
            text += f"{name} — {r['date']}\n"
        bot.reply_to(m,text)
        return
    date_text = parts[1]
    if not re.match(r"\d{2}\.\d{2}\.\d{4}$", date_text):
        bot.reply_to(m,"Используй формат: /dr дд.мм.гггг")
        return
    db_execute("INSERT OR REPLACE INTO birthdays(chat_id,user_id,date) VALUES (?,?,?)",(chat_id,user_id,date_text))
    bot.reply_to(m,f"🎂 День рождения сохранён: {date_text}")

@bot.message_handler(commands=['kto'])
def cmd_kto(m):
    res = whoami(str(m.chat.id), str(m.from_user.id))
    bot.reply_to(m,res)