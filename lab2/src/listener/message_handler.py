from random import randrange


class MessageHandler:
    def __init__(self):
        pass

    def is_message_valid(self, message: str):
        return randrange(100) > 10
