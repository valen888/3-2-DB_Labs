from redis_server.redis_client import RedisClient


class PubSub:
    def __init__(self, name: str):
        self.__redis = RedisClient.get_connection()
        self.__pubsub = self.__redis.pubsub()
        self.__name = name

    def publish(self, msg: str):
        return self.__redis.publish(self.__name, msg)

    def subscribe(self):
        return self.__pubsub.subscribe(self.__name)

    def listen(self):
        return self.__pubsub.listen()

    def get_message(self):
        return self.__pubsub.get_message()
