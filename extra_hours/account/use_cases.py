from pyflunt.notifications import Notification

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.use_cases import UseCase


class CreateUser(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        email_available = self._user_repository.check_email(command.email)

        if not email_available:
            self.add_notification(Notification('email', 'email not available'))

        email = Email(command.email)

        password = Password(command.password)

        user = User(email, password)

        self.add_notifications(user)

        if not self.is_valid:
            return

        self._user_repository.save(user)
