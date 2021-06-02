import npyscreen


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class SendMessageDisplay(npyscreen.ActionForm):
    def create(self):
        y, x = self.useable_space()
        self.receiver = self.add(npyscreen.TitleText, name="Send to:", max_height=y // 2)
        self.text = self.add(InputBox, name="Text:")

    def on_ok(self):
        receiver = self.receiver
        text = self.text
        sender = self.parentApp.username
        message = self.parentApp.message_controller
        message.send_message(text.value, sender, receiver.value)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
