from redis_server.redis_client import RedisClient


class List:
    def __init__(self, name: str):
        self.__redis = RedisClient.get_connection()
        self.__name = name

    def count(self):
        return self.__redis.llen(self.__name)

    def get_all(self, offset: int = 0, limit: int = 0):
        return self.__redis.lrange(self.__name, offset, offset + limit - 1)

    def add(self, value: str):
        return self.__redis.rpush(self.__name, value)

    def remove(self):
        return self.__redis.lpop(self.__name)

    def remove_blocking(self):
        return self.__redis.blpop(self.__name)[1].decode("utf-8")
