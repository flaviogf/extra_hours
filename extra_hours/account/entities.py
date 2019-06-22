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
