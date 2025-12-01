import os, random
from main import bot, db_execute, PHOTO_DIR

@bot.message_handler(commands=['buy'])
def cmd_buy(m):
    chat_id, user_id = m.chat.id, m.from_user.id
    choice = random.choice(['photo','boost'])
    if choice=='photo':
        photos = [os.path.join(PHOTO_DIR,f) for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg','.png','.jpeg'))]
        if not photos:
            bot.reply_to(m,"Нет фото для отправки 😅")
            return
        photo_path = random.choice(photos)
        with open(photo_path,'rb') as p:
            bot.send_photo(chat_id,p)
        bot.reply_to(m,"🎉 Вы получили рандомное фото!")
    else:
        game_choice = random.choice(['boobs','klitor','hui'])
        if game_choice=='boobs':
            delta = random.randint(-10,10)
            db_execute("UPDATE boobs SET size=size+? WHERE chat_id=? AND user_id=?", (delta,str(chat_id),str(user_id)))
            new_size = db_execute("SELECT size FROM boobs WHERE chat_id=? AND user_id=?", (str(chat_id),str(user_id)), fetch=True)[0]['size']
            bot.reply_to(m,f"🎉 Ваш размер груди изменился на <b>{delta:+d}</b>, теперь — <b>{new_size}</b> 🍒")
        elif game_choice=='klitor':
            delta = random.randint(-10,10)
            db_execute("UPDATE klitor SET size_mm=size_mm+? WHERE chat_id=? AND user_id=?", (delta,str(chat_id),str(user_id)))
            new_size = db_execute("SELECT size_mm FROM klitor WHERE chat_id=? AND user_id=?", (str(chat_id),str(user_id)), fetch=True)[0]['size_mm']
            bot.reply_to(m,f"🎉 Ваш клитор изменился на <b>{delta:+d} мм</b>, теперь — <b>{new_size}</b> 🍆")
        else:
            delta = random.randint(-10,10)
            db_execute("UPDATE hui SET size_cm=size_cm+? WHERE chat_id=? AND user_id=?", (delta,str(chat_id),str(user_id)))
            new_size = db_execute("SELECT size_cm FROM hui WHERE chat_id=? AND user_id=?", (str(chat_id),str(user_id)), fetch=True)[0]['size_cm']
            bot.reply_to(m,f"🎉 Ваш хуй изменился на <b>{delta:+d} см</b>, теперь — <b>{new_size}</b> 🍌")