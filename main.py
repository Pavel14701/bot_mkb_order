from datetime import datetime
from telebot import custom_filters
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from telebot.states.sync.context import StateContext
from bot_instance import bot, MyStates, cache_storage
from datasets.db_comands import db
from utils import del_msg, quiq_inline_keyboard, update_msg_to_del, logger


@bot.message_handler(commands=["start"])
def start_ex(message: Message|CallbackQuery):
    user_data = {
        'chat_id': 'user_id' if message.chat.id == message.from_user.id else message.chat.id,
        'user_id': message.from_user.id,
        'timestamp': datetime.now(),
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }
    inline_markup = quiq_inline_keyboard(first='hz1', second='hz2', third='hz3')
    with open('./images/first.jpg', 'rb') as photo:
        msg = bot.send_photo(
            message.chat.id,
            photo,
            caption =f'приветствие для {user_data['first_name']} {user_data['last_name']}\n\
                ',
            reply_to_message_id=message.message_id,
            reply_markup=inline_markup
        )
    update_msg_to_del(message.chat.id, message.from_user.id, msg)
    cache_storage.add_data(user_data['chat_id'], user_data['user_id'], data={'name':{'first_name': user_data['first_name'], 'last_name': user_data['last_name']}})
    db.add_user_to_base(user_data)


def start(chat_id, user_id):
    state_data = del_msg(chat_id, user_id, True)
    inline_markup = quiq_inline_keyboard(first='hz1', second='hz2', third='hz3')
    with open('./images/first.jpg', 'rb') as photo:
        msg = bot.send_photo(chat_id, photo, caption =f'приветствие для {state_data['name']['first_name']} {state_data['name']['last_name']}', reply_markup=inline_markup)
    update_msg_to_del(chat_id, user_id, msg)


def first(chat_id, user_id, state:StateContext):
    state.set(MyStates.name_company)
    del_msg(chat_id, user_id)
    inline_markup = quiq_inline_keyboard(back_to_main='Назад')
    msg = bot.send_message(chat_id, text='имя компании', reply_markup=inline_markup)
    update_msg_to_del(chat_id, user_id, msg)


@bot.message_handler(state=MyStates.name_company)
def ask_status_company(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_data={
        'name_company': message.text,
        'timestamp': datetime.now()
    }
    db.update_user_name_company(user_id, user_data)
    del_msg(chat_id, user_id)
    inline_markup = quiq_inline_keyboard(company_ooo='ООО', company_ip='ИП', back_to_main='Назад')
    msg = bot.send_message(chat_id, text='У вас ип или ООО ?', reply_markup=inline_markup)
    update_msg_to_del(chat_id, user_id, msg)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    match call.data:
        case 'first':
            state = StateContext(call, bot)
            first(chat_id, user_id, state)
        case 'back_to_main':
            start(chat_id, user_id)
        case _:
            logger.warning(f"Unhandled callback query data: {call.data}")
            print(f'\n\nWarning !!!\nUnhandled callback query data: {call.data}\n\n')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())
from telebot.states.sync.middleware import StateMiddleware
bot.setup_middleware(StateMiddleware(bot))


if __name__ == '__main__':
    bot.infinity_polling()