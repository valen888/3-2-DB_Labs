from redis_server.settings import message_blocked_status, message_in_queue_status, message_processing_status, \
    message_send_status, message_delivered_status, most_active_users, sent_message, activity_journal, message_queue, \
    spamers, incoming_message
from redis_server.wrappers.hash import Hash
from redis_server.wrappers.list import List
from redis_server.wrappers.pub_sub import PubSub
from redis_server.wrappers.set import Set
from redis_server.wrappers.zset import ZSet
from listener.message_handler import MessageHandler


class ListenerInstance:
    def __init__(self, handler: MessageHandler):
        self.__handler = handler
        self.__message_queue = List(message_queue)

        # status sets
        self.__message_in_queue_status = Set(message_in_queue_status)
        self.__messages_processing_status = Set(message_processing_status)
        self.__messages_send_status = Set(message_send_status)
        self.__messages_delivered_status = Set(message_delivered_status)
        self.__messages_blocked_status = Set(message_blocked_status)

        self.__journal = PubSub(activity_journal)
        self.__sent_message_journal_prefix = sent_message

        self.__active_users = ZSet(most_active_users)
        self.__spamers = ZSet(spamers)

        self.__incoming_message_prefix = incoming_message

    def run(self):
        while True:
            message_id = self.__message_queue.remove_blocking()
            self.__message_in_queue_status.move_to(message_processing_status, message_id)
            message = Hash(message_id)
            sender, message_body, receiver = ListenerInstance.__get_message_data(message)

            if self.__handler.is_message_valid(message_body):
                self.__messages_processing_status.move_to(message_send_status, message_id)
                List(self.__incoming_message_prefix + receiver).add(message_id)
                PubSub(self.__sent_message_journal_prefix + receiver).publish(receiver)
                self.__messages_send_status.move_to(message_delivered_status, message_id)
                self.__journal.publish("Client `%s` has sent `%s` to user `%s`" %
                                       (sender, message_body, receiver))
                self.__active_users.add(sender, 1)
            else:
                self.__messages_processing_status.move_to(message_blocked_status, message_id)
                self.__spamers.add(sender, 1)
                self.__journal.publish("Client `%s` tried to SPAM `%s` to user `%s`" %
                                       (sender, message_body, receiver))

    @staticmethod
    def __get_message_data(message: Hash):
        sender = message.get('from')
        message_body = message.get('body')
        receiver = message.get('to')
        return sender, message_body, receiver
