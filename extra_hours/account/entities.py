from pyflunt.notifications import Notification

from extra_hours.shared.entities import Entity


class User(Entity):
    def __init__(self, email, password, uid=None):
        super().__init__(uid=uid)

        self._email = email
        self._password = password

        self.add_notifications(email, password)

    @property
    def email(self):
        return str(self._email)

    @property
    def password(self):
        return str(self._password)

    def authenticate(self, password):
        if self._password == password:
            return

        self.add_notification(Notification('password', 'wrong password'))

    def __eq__(self, other):
        return self.uid == other.uid

    def change_password(self, old_password, new_password):
        self.authenticate(old_password)

        if not self.is_valid:
            return

        self._password = new_password
