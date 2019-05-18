import uuid

from extra_hours.account.value_objects import Password
from extra_hours.shared.entities import Entity


class User(Entity):
    def __init__(self, email, password):
        super().__init__()
        self._email = email
        self._password = password

        self.add_notifications(email, password)

    def resets_password(self):
        new_password = str(uuid.uuid4()).lower()[:6]
        self._password = Password(new_password)

        self.add_notifications(new_password)

    def change_password(self, password):
        self._password = password

        self.add_notifications(password)
