from datetime import datetime
from telebot import TeleBot, types, ExceptionHandler
import time
from requests.exceptions import ReadTimeout, ConnectionError


from DAO import DAO
from config import get_tg_token
from model import Participants

TOKEN = get_tg_token()
bot = TeleBot(token=TOKEN)


class MyExceptionHandler(ExceptionHandler):
    def handle(self, exc_info):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Произошло исключение: {exc_info}")
        time.sleep(1)
        return True  #



@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_auth = DAO.define_authorization(message.from_user.id)

    if user_auth == 'ADM':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('/message_to_all'),
                   types.KeyboardButton('/message_to_ref'),
                   types.KeyboardButton('/unsubscribe'))
    elif user_auth == 'REF':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('/message_to_ref'),
                   types.KeyboardButton('/unsubscribe'))
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('/unsubscribe'))

    with open('welcome_text.txt', 'r', encoding='utf-8') as f:
        message_text = f.read()
    bot.send_message(chat_id, message_text, reply_markup=markup)

    participant = Participants(
        authorization='PLR',
        tg_id_participant=message.from_user.id,
        chat_id_participant=chat_id
    )
    DAO.create_participant(participant)

@bot.message_handler(commands=['message_to_all'])
def message_to_all_init(message):
    user_auth = DAO.define_authorization(message.from_user.id)
    if user_auth == 'ADM':
        bot.send_message(message.chat.id, "ну пиши мне то че")
        bot.register_next_step_handler(message, send_to_all)


def send_to_all(message):
    results = DAO.find_all_participants()
    if results:
        for result in results:
            try:
                bot.send_message(result.chat_id_participant, message.text)
                time.sleep(0.05)
            except (ReadTimeout, ConnectionError) as e:
                print(f"Ошибка отправки {result.chat_id_participant}: {e}")
                time.sleep(1)

@bot.message_handler(commands=['message_to_ref'])
def message_to_ref_init(message):
    user_auth = DAO.define_authorization(message.from_user.id)
    if user_auth in ['ADM', 'REF']:
        bot.send_message(message.chat.id, "Че ты там пишешь:")
        bot.register_next_step_handler(message, send_to_ref)

def send_to_ref(message):
    results = DAO.find_all_refery()
    if results:
        for result in results:
            try:
                bot.send_message(result.chat_id_participant, message.text)
                time.sleep(0.05)
            except (ReadTimeout, ConnectionError) as e:
                print(f"Ошибка отправки {result.chat_id_participant}: {e}")
                time.sleep(1)

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    caption = message.caption if message.caption else ""
    photo = message.photo[-1].file_id if message.photo else None
    if photo is None:
        bot.reply_to(message, "Фото не получено.")
        return

    user_auth = DAO.define_authorization(message.from_user.id)
    if user_auth == 'ADM':
        results = DAO.find_all_participants()
        if results:
            for result in results:
                try:
                    bot.send_photo(result.chat_id_participant, photo, caption=caption)
                    time.sleep(0.05)
                except (ReadTimeout, ConnectionError) as e:
                    print(f"Ошибка отправки фото {result.chat_id_participant}: {e}")
                    time.sleep(1)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    DAO.delete_participant(message.from_user.id)
    bot.send_message(message.chat.id, 'Еще увидимся!')

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)