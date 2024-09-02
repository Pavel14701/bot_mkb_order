import telebot, os, redis
from telebot.storage import StateRedisStorage
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from dotenv import load_dotenv
load_dotenv()


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
state_storage = StateRedisStorage(redis_client)
bot = telebot.TeleBot(os.getenv('TOKEN'), state_storage=state_storage, num_threads=20)


class MyStates(State):
    pass
