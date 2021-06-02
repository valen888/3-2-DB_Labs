from redis_server.redis_client import RedisClient


class Hash:
    def __init__(self, name: str):
        self.__redis = RedisClient.get_connection()
        self.__name = name

    def delete(self, key: str):
        return self.__redis.hdel(self.__name, key)

    def get(self, key: str):
        return self.__redis.hget(self.__name, key).decode("utf-8")

    def set(self, key: str, value: str):
        return self.__redis.hset(self.__name, key, value)

    def set_all(self, payload: dict):
        return self.__redis.hmset(self.__name, payload)
