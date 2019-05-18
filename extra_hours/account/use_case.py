from pyflunt.notifications import Notification

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.use_case import UseCase


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


class AuthenticateUser(UseCase):
    def __init__(self, user_service):
        super().__init__()
        self._user_service = user_service

    def execute(self, command):
        email = Email(command.email)
        password = Password(command.password)

        self.add_notifications(email, password)

        if not self.is_valid:
            return

        user = self._user_service.sign_with_email_and_password(str(email), str(password))

        if not user:
            self.add_notification(Notification('user', 'email or password invalid'))

        return user


class ResetsPassword(UseCase):
    def __init__(self, user_service):
        super().__init__()
        self._user_service = user_service

    def execute(self, command):
        email = Email(command.email)

        self.add_notifications(email)

        if not self.is_valid:
            return

        self._user_service.send_password_reset_email(str(email))
