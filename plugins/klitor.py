from main import bot, change_size, get_display_name

@bot.message_handler(commands=['klitor'])
def cmd_klitor(m):
    chat_id, user_id = m.chat.id, m.from_user.id
    name = get_display_name(chat_id, user_id)
    delta, new_size = change_size("klitor", chat_id, user_id, (-10,10))
    if delta == 0:
        bot.reply_to(m, f"Ой, а ты уже пробовал сегодня 😅\nТекущий клитор — <b>{new_size} мм</b> 🍆")
    else:
        bot.reply_to(m, f"🍆 {name}, твой клитор изменился на <b>{delta:+d} мм</b>, теперь — <b>{new_size} мм</b> 🍆")