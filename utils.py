import contextlib, logging
from typing import Optional
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot_instance import cache_storage, bot


def update_msg_to_del(chat_id:int, user_id:int, msg: Message):
    key = 'msg_del'
    value = {'chat_id':msg.chat.id, 'message_id': msg.message_id}
    cache_storage.add_data(chat_id, user_id, key, value)


def del_msg(chat_id:int, user_id:int, return_state_data:bool=False) -> Optional[dict]:
    msg = cache_storage.get_data(chat_id, user_id).get('msg_del')
    with contextlib.suppress():
        bot.delete_message(int(msg['chat_id']), msg['message_id'])
    if return_state_data:
        return msg


def quiq_inline_keyboard(**kwargs):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for callback_data, text in kwargs.items():
        button = InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
        inline_markup.add(button)
    return inline_markup

def create_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('logs.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = create_logger()