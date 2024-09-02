import telebot, os, json
from redis import Redis
from telebot.storage import StateRedisStorage
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from typing import Any
from contextlib import contextmanager
from dotenv import load_dotenv
load_dotenv()


state_storage = StateRedisStorage(host=os.getenv('host'), port=6379, db=2)
bot = telebot.TeleBot(os.getenv('TOKEN'), state_storage=state_storage, num_threads=20)


class MyStates(State):
    name_company = State()


class RedisCache:
    def __init__(self, bot:telebot.TeleBot=bot):
        self.bot = bot
        self.bot_id = self.bot.bot_id


    @contextmanager
    def redis_connection(self):
        conn = Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))
        try:
            yield conn
        finally:
            conn.close()


    def add_data(self, user_id:int, chat_id:int, data:Any) -> None:
        with self.redis_connection() as cache:
            key = f'{self.bot_id}_{user_id}_{chat_id}'
            cache.set(key, json.dumps(data))
            print(f"Value set in cache: {key} -> {data}")


    def get_data(self, user_id:int, chat_id:int) -> Any:
        with self.redis_connection() as cache:
            key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(key):
                return json.loads(json_data)

cache_storage = RedisCache()