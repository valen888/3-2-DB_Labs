from listener.message_handler import MessageHandler
from listener.listener import ListenerInstance

if __name__ == '__main__':
    handler = MessageHandler()
    worker = ListenerInstance(handler)
    worker.run()
