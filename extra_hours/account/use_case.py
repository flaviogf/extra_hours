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

        token = self._user_service.sign_with_email_and_password(str(email), str(password))

        if not token:
            self.add_notification(Notification('user', 'email or password invalid'))

        return token


class ResetsPassword(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        email = Email(command.email)

        self.add_notifications(email)

        if not self.is_valid:
            return

        user = self._user_repository.find_by_email(str(email))

        if not user:
            self.add_notification(Notification('user', 'user not found'))
            return

        user.resets_password()

        self._user_repository.save(user)


class ChangeUserPassword(UseCase):
    def __init__(self, user_repository, user_service):
        super().__init__()
        self._user_repository = user_repository
        self._user_service = user_service

    def execute(self, command):
        email = Email(command.email)
        old_password = Password(command.old_password)

        self.add_notifications(email, old_password)

        if not self.is_valid:
            return

        user = self._user_service.sign_with_email_and_password(str(email), str(old_password))

        if not user:
            self.add_notification(Notification('user', 'email or password invalid'))
            return

        new_password = Password(command.new_password)

        user.change_password(new_password)

        self.add_notifications(user)

        if not self.is_valid:
            return

        self._user_repository.save(user)
