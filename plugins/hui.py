from main import bot, change_size, get_display_name

@bot.message_handler(commands=['hui'])
def cmd_hui(m):
    chat_id, user_id = m.chat.id, m.from_user.id
    name = get_display_name(chat_id, user_id)
    delta, new_size = change_size("hui", chat_id, user_id, (-10,10))
    if delta == 0:
        bot.reply_to(m, f"Ой, а ты уже пробовал сегодня 😅\nТекущий хуй — <b>{new_size} см</b> 🍌")
    else:
        bot.reply_to(m, f"🍌 {name}, твой хуй изменился на <b>{delta:+d} см</b>, теперь — <b>{new_size} см</b> 🍌")