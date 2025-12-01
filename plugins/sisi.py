from main import bot, change_size, get_display_name

@bot.message_handler(commands=['sisi'])
def cmd_sisi(m):
    chat_id, user_id = m.chat.id, m.from_user.id
    name = get_display_name(chat_id, user_id)
    delta, new_size = change_size("boobs", chat_id, user_id)
    if delta == 0:
        bot.reply_to(m, f"Ой, а ты уже пробовал сегодня 😅\nТвой текущий размер груди — <b>{new_size}</b> 🍒")
    else:
        bot.reply_to(m, f"🍒 {name}, твой размер груди изменился на <b>{delta:+d}</b>, теперь — <b>{new_size}</b> 🍒")