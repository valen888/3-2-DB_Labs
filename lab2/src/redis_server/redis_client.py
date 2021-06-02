import redis

from constants import DB_HOST, DB_PORT, DB_SCHEMA_NAME, DB_PASSWORD


class RedisClient:
    __instance = None

    def __init__(self):
        if not RedisClient.__instance:
            self.__conn = redis.Redis(host=DB_HOST, port=DB_PORT, db=DB_SCHEMA_NAME, password=DB_PASSWORD)

    @classmethod
    def get_connection(cls):
        if not cls.__instance:
            cls.__instance = RedisClient()
        return cls.__instance.__conn

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = RedisClient()
        return cls.__instance
