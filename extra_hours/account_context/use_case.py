from pyflunt.notifications import Notification

from extra_hours.account_context.entities import User
from extra_hours.account_context.value_objects import Email, Password
from extra_hours.shared_context.use_case import UseCase


class CreateUser(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        email_available = self._user_repository.check_email(command.email)

        if not email_available:
            self.add_notifications(Notification('email',
                                                'email not is available'))
            return

        email = Email(command.email)
        password = Password(command.password)

        user = User(email=email,
                    password=password)

        self.add_notifications(user)

        if not self.is_valid:
            return

        self._user_repository.save(user)


class AuthenticateUser:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def execute(self, command):
        self._user_repository.find_by_credentials()

        # TODO: steps to authenticate user
