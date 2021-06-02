from redis_server.redis_client import RedisClient


class Set:
    def __init__(self, name: str):
        self.__redis = RedisClient.get_connection()
        self.__name = name

    def add(self, value: str):
        return self.__redis.sadd(self.__name, value)

    def contains(self, value: str):
        return self.__redis.sismember(self.__name, value)

    def get_all(self):
        # use SSCAN to iterate when sets are to huge
        return [x.decode("utf-8") for x in self.__redis.smembers(self.__name)]

    def remove(self, value: str):
        return self.__redis.srem(self.__name, value)

    def get_name(self):
        return self.__name

    def union(self, set_names: [str], key_store: str):
        return self.__redis.sunionstore(key_store, set_names)

    def intersect(self, set_names: [str], key_store: str):
        count = self.__redis.sinterstore(key_store, set_names)
        return count

    def move_to(self, dest: str, value: str):
        return self.__redis.smove(self.__name, dest, value)
