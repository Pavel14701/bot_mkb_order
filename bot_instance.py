import os, json, telebot, redis
from redis.connection import ConnectionPool
from typing import Any, Optional
from telebot.storage import StateRedisStorage
from telebot.states import State, StatesGroup
from dotenv import load_dotenv


load_dotenv()
state_storage = StateRedisStorage(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))
bot = telebot.TeleBot(os.getenv('TOKEN'), state_storage=state_storage, num_threads=20, use_class_middlewares=True, colorful_logs=True)


class MyStates(StatesGroup):
    name_company = State()


class RedisCache:
    def __init__(self, bot:telebot.TeleBot=bot):
        self.bot = bot
        self.bot_id = self.bot.bot_id
        self.pool = ConnectionPool(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))


    def __worker(self):
        return redis.Redis(connection_pool=self.pool)


    def add_data(self, user_id:int, chat_id:int, key:Optional[str]=None, value:Any=None) -> None:
        data = {f'{key}': value} if key else value
        conn = self.__worker()
        with conn as cache:
            key = f'{self.bot_id}_{user_id}_{chat_id}'
            cache.set(key, json.dumps(data))


    def get_data(self, user_id: int, chat_id: int) -> Any:
        conn = self.__worker()
        with conn as cache:
            key = f'{self.bot_id}_{user_id}_{chat_id}'
            if json_data := cache.get(key):
                return json.loads(json_data)


    def delete_data(self, user_id:int, chat_id:int) -> None:
        conn = self.__worker()
        with conn as cache:
            key = f'{self.bot_id}_{user_id}_{chat_id}'
            cache.delete(key)


cache_storage = RedisCache()