import signal
import sys

import npyscreen

from constants import main_form, message_form, send_message_form, admin_form
from redis_server.controllers.client import Client
from redis_server.controllers.message import Message
from views import auth
from views.admin import AdminDisplay
from views.message import MessageListDisplay
from views.send_message import SendMessageDisplay


class App(npyscreen.StandardApp):
    def __init__(self):
        super().__init__()
        signal.signal(signal.SIGINT, self.__handle_interrupt_event)
        signal.signal(signal.SIGTERM, self.__handle_interrupt_event)
        self.client_controller = Client()
        self.message_controller = Message()
        self.username = ''

    def onStart(self):
        self.addForm(main_form, auth.AuthDisplay, name="Auth")
        self.addFormClass(message_form, MessageListDisplay, name="Main")
        self.addFormClass(send_message_form, SendMessageDisplay, name="Send Message")
        self.addFormClass(admin_form, AdminDisplay, name="Admin")

    def __handle_interrupt_event(self, _sig, _frame):
        self.onCleanExit()
        sys.exit(0)

    def onCleanExit(self):
        if isinstance(self.username, str):
            self.client_controller.logout(self.username)


if __name__ == '__main__':
    myApp = App()
    myApp.run()
