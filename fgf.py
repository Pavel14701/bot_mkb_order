import telebot, os
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
#from telebot.storage import StateRedisStorage
#import redis
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
#pip install python-dotenv
#создай в корневой директории файл .env и сохрани свой токен так TOKEN=hwifhwuifhefne

# Initialize the bot
# Если думаешь юзать редис, нужно ставить редис как микросервис, отдельно его заводить и подключаться
# pip install redis
load_dotenv()
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) #Стандарт класик редиса, локальное подключение, стандартный порт и база данных
#state_storage = StateRedisStorage(redis_client)
bot = telebot.TeleBot(str(os.getenv('TOKEN')), state_storage=state_storage, use_class_middlewares=True)



# Для базы данных для тестов можно использовать движок sqlite
# но если ты учишся лучше сразу юзай mysql или postgres
# они тоже ставятся как микросервисы и ты должен отдельно к ним подключаться
# Define states
class MyStates(StatesGroup):
    #здесь глобальные данны(only states here)
    name_company = State()#{}
    machine = State()#{}
    prifugovka = State()#да нет
    your_prifugovka_na_tolshini_kromki = State()#да нет
    prifugovka_tolshini_kromki = State()# 0.5 1 2
    tolshina_kromki_vidimaya_storona = State()#{}
    list_btn_genre = State()  # переменная для списка кнопка по жанрам взятых с сайта
    # Стейты обязательно должны быть экземпляром класса то что юзер отвечает ты должен принимать и 
    # каким-то образом проверять, обрабатывать

# Start command handler
@bot.message_handler(commands=["start"])
def start_ex(message: types.Message, state: StateContext):
    state.set(MyStates.name_company)
    bot.send_message(
        message.chat.id,
        "Hello! What is your first name?",
        reply_to_message_id=message.message_id,
    )


# Cancel command handler
@bot.message_handler(state="*", commands=["cancel"])
def any_state(message: types.Message, state: StateContext):
    state.delete()
    bot.send_message(
        message.chat.id,
        "Your information has been cleared. Type /start to begin again.",
        reply_to_message_id=message.message_id,
    )


# Handler for name input
@bot.message_handler(state=MyStates.name_company)
def name_get(message: types.Message, state: StateContext):
    state.set(MyStates.machine)
    bot.send_message(
        message.chat.id, "How old are you?", reply_to_message_id=message.message_id
    )
    state.add_data(name_company=message.text)


# Handler for age input
@bot.message_handler(state=MyStates.machine, is_digit=True)
def ask_color(message: types.Message, state: StateContext):
    state.set(MyStates.prifugovka)
    state.add_data(machine=message.text)

    # Define reply keyboard for color selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    prifugovki = ["Your", "Own", "Variable", "Data"]
    buttons = [types.KeyboardButton(prifugovka) for prifugovka in prifugovki]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "What is your favorite color? Choose from the options below.",
        reply_markup=keyboard,
        reply_to_message_id=message.message_id,
    )


# Handler for color input
@bot.message_handler(state=MyStates.prifugovka)
def ask_hobby(message: types.Message, state: StateContext):
    state.set(MyStates.your_prifugovka_na_tolshini_kromki)
    state.add_data(color=message.text)

    # Define reply keyboard for hobby selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    hobbies = ["HZ1", "HZ2", "HZ3", "HZ4"]
    buttons = [types.KeyboardButton(hobby) for hobby in hobbies]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "What is one of your hobbies? Choose from the options below.",
        reply_markup=keyboard,
        reply_to_message_id=message.message_id,
    )


# Handler for hobby input
@bot.message_handler(
    state=MyStates.your_prifugovka_na_tolshini_kromki, text=["HZ1", "HZ2", "HZ3", "HZ4"]
)
def finish(message: types.Message, state: StateContext):
    with state.data() as data:
        name_company = data.get("name_company")
        machine = data.get("machine")
        prifugovka = data.get("prifugovka")
        your_prifugovka_na_tolshini_kromki = message.text  # Get the hobby from the message text

        # Provide a fun fact based on color
        color_facts = {
            "Red": "Red is often associated with excitement and passion.",
            "Green": "Green is the color of nature and tranquility.",
            "Blue": "Blue is known for its calming and serene effects.",
            "Yellow": "Yellow is a cheerful color often associated with happiness.",
            "Purple": "Purple signifies royalty and luxury.",
            "Orange": "Orange is a vibrant color that stimulates enthusiasm.",
            "Other": "Colors have various meanings depending on context.",
        }
        # тут идёт сравнение введённых параметров с ключом в дикте,
        # если есть совпадение он выдаст значение
        color_fact = color_facts.get(
            prifugovka, "Colors have diverse meanings, and yours is unique!"
        )

        msg = (
            f"Thank you for sharing! Here is a summary of your information:\n"
            f"name_company: {name_company}\n"
            f"Machine: {machine}\n"
            f"Prifugovka: {prifugovka}\n"
            f"Color_fact: {color_fact}\n"
            f"your_prifugovka_na_tolshini_kromki: {your_prifugovka_na_tolshini_kromki}"
        )

    bot.send_message(
        message.chat.id, msg, parse_mode="html", reply_to_message_id=message.message_id
    )
    state.delete()


# Handler for incorrect age input
@bot.message_handler(state=MyStates.machine, is_digit=False)
def age_incorrect(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Please enter a valid number for age.",
        reply_to_message_id=message.message_id,
    )


# Add custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))

# Start polling
bot.infinity_polling()
