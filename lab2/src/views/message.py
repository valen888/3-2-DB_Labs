import npyscreen

from constants import admin_form, send_message_form
from redis_server.settings import statuses, sent_message
from redis_server.wrappers.pub_sub import PubSub


class MessageList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(MessageList, self).__init__(*args, **keywords)


class SelectMessageType(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne

    def __init__(self, *args, **keywords):
        super(SelectMessageType, self).__init__(*args, **keywords)

    def when_value_edited(self):
        username = self.parent.parentApp.username
        message = self.parent.parentApp.message_controller
        count = message.count_messages_in_status(username, statuses[self.value[0]])
        self.name = "Total: %i" % count
        self.update()


class SendMessageButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm(send_message_form)


class ToAdminFormButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm(admin_form)


class MessageListDisplay(npyscreen.FormBaseNew):
    def create(self):
        self.__journal_pub_sub = PubSub(sent_message + self.parentApp.username)
        self.__journal_pub_sub.subscribe()
        y, x = self.useable_space()
        self.list = self.add(MessageList, max_width=x // 2, max_height=y // 2)
        self.select = self.add(SelectMessageType,
                               values=statuses,
                               value=[0],
                               relx=x // 2 + 2, rely=2, max_height=y // 2)
        self.add(SendMessageButton, name="Send Message", rely=-3)

        is_admin = self.parentApp.client_controller.is_admin(self.parentApp.username)
        if is_admin:
            self.add(ToAdminFormButton, name="To Admin", relx=x//2 + 1, rely=-3)

    def beforeEditing(self):
        self.update_list(True)

    def update_list(self, init=False):
        if self.__read_all_messages_from_journal() or init:
            message = self.parentApp.message_controller
            username = self.parentApp.username
            self.list.values = message.read_messages(username)
            self.list.display()

    def while_waiting(self):
        self.update_list()

    def __read_all_messages_from_journal(self):
        messages = []
        message = self.__journal_pub_sub.get_message()
        while message is not None:
            messages.append(message)
            message = self.__journal_pub_sub.get_message()

        return len(messages) != 0
