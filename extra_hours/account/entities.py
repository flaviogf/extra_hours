from extra_hours.shared.entities import Entity


class User(Entity):
    def __init__(self, email, password):
        super().__init__()
        self._email = email
        self._password = password

        self.add_notifications(email, password)
