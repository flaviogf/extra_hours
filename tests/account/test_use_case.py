import unittest
from unittest.mock import Mock

from extra_hours.account.commands import (AuthenticateUserCommand,
                                          CreateUserCommand)
from extra_hours.account.entities import User
from extra_hours.account.use_case import AuthenticateUser, CreateUser


class CreateUserTests(unittest.TestCase):
    def setUp(self):
        self._command = CreateUserCommand(email='captain@marvel.com.br',
                                          password='test123!')

        self._user_repository = Mock()

        self._create_user = CreateUser(self._user_repository)

    def test_should_ensure_check_email(self):
        self._create_user.execute(self._command)

        self._user_repository.check_email.assert_called_once()

    def test_should_ensure_save_user(self):
        self._create_user.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_is_valid_false_when_command_not_is_valid(self):
        command = CreateUserCommand(email='captain',
                                    password='test123')

        self._create_user.execute(command)

        self.assertFalse(self._create_user.is_valid)

    def test_should_is_valid_false_when_email_not_is_available(self):
        self._user_repository.check_email.return_value = False

        self._create_user.execute(self._command)

        self.assertFalse(self._create_user.is_valid)

    def test_should_is_valid_true_when_command_is_valid(self):
        self._create_user.execute(self._command)

        self.assertTrue(self._create_user.is_valid)


class AuthenticateUserTests(unittest.TestCase):
    def setUp(self):
        self._command = AuthenticateUserCommand(email='captain@marvel.com.br',
                                                password='test123')

        self._user_service = Mock()

        self._authenticate_user = AuthenticateUser(self._user_service)

    def test_should_ensure_sign_user_with_email_and_password(self):
        self._authenticate_user.execute(self._command)

        self._user_service.sign_with_email_and_password.assert_called_with(self._command.email,
                                                                           self._command.password)

    def test_should_is_valid_false_when_user_not_is_authenticated(self):
        self._user_service.sign_with_email_and_password.return_value = None

        self._authenticate_user.execute(self._command)

        self.assertFalse(self._authenticate_user.is_valid)

    def test_should_is_valid_false_when_email_not_is_valid(self):
        command = AuthenticateUserCommand(email='test',
                                          password='test123')

        self._authenticate_user.execute(command)

        self.assertFalse(self._authenticate_user.is_valid)

    def test_should_is_valid_false_when_password_not_is_valid(self):
        command = AuthenticateUserCommand(email='captain@marvel.com',
                                          password='test')

        self._authenticate_user.execute(command)

        self.assertFalse(self._authenticate_user.is_valid)

    def test_should_return_user_when_authenticate(self):
        self._user_service.sign_with_email_and_password.return_value = User(email=self._command.email,
                                                                            password=self._command.password)

        user = self._authenticate_user.execute(self._command)

        self.assertIsInstance(user, User)
