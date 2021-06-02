from redis_server.settings import users_set, admins_set, online_users, activity_journal, most_active_users, spamers
from redis_server.wrappers.pub_sub import PubSub
from redis_server.wrappers.set import Set
from redis_server.wrappers.zset import ZSet


class Client:
    def __init__(self):
        self.__users = Set(users_set)
        self.__admins = Set(admins_set)
        self.__online_users = Set(online_users)
        self.__journal = PubSub(activity_journal)
        self.__active_users = ZSet(most_active_users)
        self.__spamers = ZSet(spamers)

    def is_admin(self, username: str):
        return self.__admins.contains(username)

    def is_user(self, username: str):
        return self.__users.contains(username)

    def is_registered(self, username: str):
        return self.is_admin(username) or self.is_user(username)

    def register(self, username: str, is_admin=False):
        set_to_save: Set = self.__admins if is_admin else self.__users
        if not self.is_registered(username):
            set_to_save.add(username)
        else:
            raise Exception("Client with username '%s' has already registered" % username)

    def login(self, username: str):
        if not self.is_registered(username):
            return None

        self.__online_users.add(username)
        self.__journal.publish("Client `%s` login in chat" % username)
        return True

    def logout(self, username: str):
        self.__online_users.remove(username)
        self.__journal.publish("Client `%s` logout in chat" % username)

    def get_all_users(self):
        return self.__users.get_all()

    def get_all_online_users(self):
        return self.__online_users.get_all()

    def get_spamers(self, n: int):
        return self.__spamers.get_all_descending(0, n-1)

    def get_active_users(self, n: int):
        return self.__active_users.get_all_descending(0, n - 1)
