import npyscreen

from constants import send_message_form, message_form
from redis_server.settings import statuses, activity_journal
from redis_server.wrappers.pub_sub import PubSub


class MessageList(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineAction

    def __init__(self, *args, **keywords):
        super(MessageList, self).__init__(*args, **keywords)


class SpinBox(npyscreen.TitleSlider):
    def __init__(self, *args, **keywords):
        super(SpinBox, self).__init__(*args, **keywords)

    def when_value_edited(self):
        self.parent.update_list(True)


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


class ToMessageFormButton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm(message_form)


class AdminDisplay(npyscreen.FormBaseNew):
    __journal_pub_sub = PubSub(activity_journal)

    def create(self):
        self.__journal_pub_sub.subscribe()
        y, x = self.useable_space()

        self.__users_online = self.add(MessageList, name="Users online",
                                       relx=1, rely=1,
                                       width=x // 2 - 1, height=y // 2 - 1)

        self.__journal = self.add(MessageList, name="Journal",
                                  relx=x // 2 + 1, rely=1,
                                  width=x // 2 - 1, height=y // 2 - 1)

        self.__spamers = self.add(MessageList, name="Spamers",
                                  relx=1, rely=y // 2,
                                  width=x // 2 - 1, height=y // 2 - 3)

        self.__users_rate = self.add(MessageList, name="Active users",
                                     relx=x // 2 + 1, rely=y // 2,
                                     width=x // 2 - 1, height=y // 2 - 3)

        self.__spinbox = self.add(SpinBox, name="Count", relx=1, rely=-3, width=x // 2 - 1, value=5)
        self.add(ToMessageFormButton, name="To Message", relx=x // 2 + 1, rely=-3)

    def beforeEditing(self):
        self.update_list(True)

    def update_list(self, init=False):
        if self.__read_all_messages_from_journal() or init:
            self.__users_online.values = self.parentApp.client_controller.get_all_online_users()
            self.__users_online.update()

            self.__users_rate.values = self.parentApp.client_controller.get_active_users(int(self.__spinbox.value))
            self.__users_rate.update()

            self.__spamers.values = self.parentApp.client_controller.get_spamers(int(self.__spinbox.value))
            self.__spamers.update()

    def while_waiting(self):
        self.update_list()

    def __read_all_messages_from_journal(self):
        message = self.__journal_pub_sub.get_message()
        messages = []
        while message is not None:
            messages.append(message)
            message = self.__journal_pub_sub.get_message()

        if len(messages) == 0:
            return False
        for x in messages:
            if isinstance(x['data'], bytes):
                self.__journal.values.append(x['data'].decode("utf-8"))
        self.__journal.footer = "Total messages: %i" % len(self.__journal.values)
        self.__journal.update()
        return True
