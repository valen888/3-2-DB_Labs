import npyscreen

from constants import message_form


class AuthDisplay(npyscreen.ActionForm):
    def create(self):
        self.title = self.add(npyscreen.TitleText, name="Login")

    def on_ok(self):
        username = self.title.value
        client = self.parentApp.client_controller
        if client.is_registered(username):
            client.login(username)
        else:
            message_to_display = 'Set as Admin user?'
            is_admin = npyscreen.notify_yes_no(message_to_display, title='Choose yes or no')
            client.register(username, is_admin)
            client.login(username)

        self.parentApp.username = username
        self.parentApp.setNextForm(message_form)
