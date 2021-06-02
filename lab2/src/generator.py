import sys
import signal
from random import randrange
from time import sleep

from redis_server.controllers.client import Client
from redis_server.controllers.message import Message
from redis_server.redis_client import RedisClient

usernames = []


def handle_interrupt_event(_sig, _frame):
    client_controller = Client()
    for x in usernames:
        client_controller.logout(x)
    sys.exit(0)


def send_messages(count_users: int):
    user_prefix = "user_id_"
    client_controller = Client()
    message_controller = Message()
    for idx in range(count_users):
        usernames.append(user_prefix + str(idx))
        client_controller.register(usernames[idx])
        client_controller.login(usernames[idx])
    index = 0
    while True:
        from_username = user_prefix + str(randrange(len(usernames)))
        to_username = from_username
        while to_username != from_username:
            to_username = user_prefix + str(randrange(len(usernames)))
        message = "test-id" + str(index)
        index += 1
        message_controller.send_message(message, from_username, to_username)
        sleep(2)


if __name__ == "__main__":
    try:
        max_users = 250
    except Exception as e:
        print(e)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_interrupt_event)
    signal.signal(signal.SIGTERM, handle_interrupt_event)
    RedisClient.get_connection().flushall()
    send_messages(max_users)
