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
            self.add_notifications(Notification('email', 'email not is available'))

        email = Email(command.email)

        password = Password(command.password)

        user = User(email=email, password=password)

        self.add_notifications(user)

        if not self.is_valid:
            return

        self._user_repository.add(user)


class AuthenticateUser(UseCase):
    def __init__(self, user_repository, token_service):
        super().__init__()

        self._user_repository = user_repository
        self._token_service = token_service

    def execute(self, command):
        email = Email(command.email)

        user = self._user_repository.get_by_email(str(email))

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return None

        password = Password(command.password)

        user.authenticate(password)

        self.add_notifications(user)

        if not self.is_valid:
            return None

        token = self._token_service.encode(user)

        return token


class ResetsPassword(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        email = Email(command.email)

        user = self._user_repository.get_by_email(str(email))

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        user.resets_password()

        self._user_repository.add(user)


class ChangeUserPassword(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        email = Email(command.email)

        user = self._user_repository.get_by_email(str(email))

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        old_password = Password(command.old_password)

        new_password = Password(command.new_password)

        user.change_password(old_password, new_password)

        self.add_notifications(user)

        if not self.is_valid:
            return

        self._user_repository.add(user)
