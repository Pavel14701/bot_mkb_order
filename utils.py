import contextlib, logging
from typing import Optional
from bot_instance import cache_storage, bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

def update_msg_to_del(chat_id:int, user_id:int, msg: Message):
    cache_storage.add_data(chat_id, user_id, data={'msg_del': {'chat_id':msg.chat.id, 'message_id': msg.message_id}})


def del_msg(chat_id:int, user_id:int, return_state_data:bool=False) -> Optional[dict]:
    state_data = cache_storage.get_data(chat_id, user_id)
    with contextlib.suppress():
        bot.delete_message(int(state_data['msg_del']['chat_id']), state_data['msg_del']['message_id'])
    if return_state_data:
        return state_data


def quiq_inline_keyboard(**kwargs):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for callback_data, text in kwargs.items():
        button = InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
        inline_markup.add(button)
    return inline_markup

logger = logging.getLogger('my_logger')
logger.setLevel(logging.ERROR)

handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

logger.addHandler(handler)