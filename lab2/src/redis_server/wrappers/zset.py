from redis_server.redis_client import RedisClient


class ZSet:
    def __init__(self, name: str):
        self.__redis = RedisClient.get_connection()
        self.__name = name

    def add(self, username: str, value: int):
        return self.__redis.zadd(self.__name, {username: value}, incr=True)

    def increment(self, username: str):
        return self.__redis.zincrby(self.__name, 1, username)

    def count(self):
        return self.__redis.zcard(self.__name)

    def get_score(self, username: str):
        return self.__redis.zscore(self.__name, username)

    def get_all_descending(self, start: int = 0, limit: int = -1):
        return [val[0].decode("utf-8").ljust(25) + str(val[1])
                for val in self.__redis.zrevrange(self.__name, start, limit, withscores=True,
                                                  score_cast_func=lambda x: int(x))]
