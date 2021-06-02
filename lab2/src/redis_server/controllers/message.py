import uuid

from redis_server.settings import message_created_status, message_in_queue_status, message_queue, message_prefix, \
    incoming_message, outgoing_message
from redis_server.wrappers.hash import Hash
from redis_server.wrappers.list import List
from redis_server.wrappers.set import Set


class Message:
    def __init__(self):
        self.__message_prefix = message_prefix
        self.__incoming_message = incoming_message
        self.__outgoing_message = outgoing_message

        self.__message_queue = List(message_queue)

        self.__messages_created_status = Set(message_created_status)
        self.__messages_in_queue_status = Set(message_in_queue_status)

    def send_message(self, text: str, sender_username: str, receiver_username: str):
        message_id = self.__message_prefix + str(uuid.uuid4())
        message = Hash(message_id)
        message.set_all({
            'from': sender_username,
            'to': receiver_username,
            'body': text
        })
        Set(self.__outgoing_message + sender_username).add(message_id)
        self.__messages_created_status.add(message_id)
        self.__message_queue.add(message_id)
        self.__messages_created_status.move_to(self.__messages_in_queue_status.get_name(), message_id)

    def read_messages(self, username: str):
        incoming_messages_list = List(self.__incoming_message + username)
        messages = incoming_messages_list.get_all()
        return [Hash(message_id).get('body') for message_id in messages]

    def count_messages_in_status(self, username: str, status: str):
        return Set(status).intersect([self.__outgoing_message + username, status], 'temp')
