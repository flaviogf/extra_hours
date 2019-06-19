import unittest
from unittest.mock import Mock

from extra_hours.account.commands import (AuthenticateUserCommand,
                                          CreateUserCommand,
                                          ResetsPasswordCommand,
                                          ChangeUserPasswordCommand)
from extra_hours.account.entities import User
from extra_hours.account.use_case import (AuthenticateUser,
                                          CreateUser,
                                          ResetsPassword,
                                          ChangeUserPassword)
from extra_hours.account.value_objects import Email, Password


class CreateUserTests(unittest.TestCase):
    def setUp(self):
        self._command = CreateUserCommand(email='captain@marvel.com.br',
                                          password='test123!')

        self._user_repository = Mock()

        self._create_user = CreateUser(self._user_repository)

    def test_should_ensure_check_email(self):
        self._create_user.execute(self._command)

        self._user_repository.check_email.assert_called_once()

    def test_should_ensure_add_user(self):
        self._create_user.execute(self._command)

        self._user_repository.add.assert_called_once()

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

        self._user_repository = Mock()
        self._token_service = Mock()

        self._authenticate_user = AuthenticateUser(user_repository=self._user_repository,
                                                   token_service=self._token_service)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.get_by_email.return_value = None

        self._authenticate_user.execute(self._command)

        self.assertFalse(self._authenticate_user.is_valid)

    def test_should_is_valid_false_when_user_not_authenticate(self):
        email = Email('captain@marvel.com')

        password = Password('test1234')

        steve = User(email=email, password=password)

        self._user_repository.get_by_email.return_value = steve

        self._token_service.encode.return_value = 'xpto-xpto'

        self._authenticate_user.execute(self._command)

        self.assertFalse(self._authenticate_user.is_valid)

    def test_should_is_valid_true_when_user_authenticate(self):
        email = Email('captain@marvel.com')

        password = Password('test123')

        steve = User(email=email, password=password)

        self._user_repository.find_by_email.return_value = steve

        self._token_service.encode.return_value = 'xpto-xpto'

        self._authenticate_user.execute(self._command)

        self.assertTrue(self._authenticate_user.is_valid)

    def test_should_return_token_when_user_authenticate(self):
        email = Email('captain@marvel.com')

        password = Password('test123')

        steve = User(email=email, password=password)

        self._user_repository.find_by_email.return_value = steve

        self._token_service.encode.return_value = 'xpto-xpto'

        token = self._authenticate_user.execute(self._command)

        self.assertIsInstance(token, str)


class ResetsPasswordTests(unittest.TestCase):
    def setUp(self):
        self._user = User(email='captain@marvel.com',
                          password='test123456')

        self._command = ResetsPasswordCommand(email='captain@marvel.com')

        self._user_repository = Mock()
        self._user_repository.find_by_email.return_value = self._user

        self._resets_password = ResetsPassword(self._user_repository)

    def test_should_ensure_find_by_email(self):
        self._resets_password.execute(self._command)

        self._user_repository.get_by_email.assert_called_with(self._command.email)

    def test_should_ensure_add_user(self):
        self._resets_password.execute(self._command)

        self._user_repository.add.assert_called_once()

    def test_should_valid_false_when_user_not_found(self):
        self._user_repository.get_by_email.return_value = None

        self._resets_password.execute(self._command)

        self.assertFalse(self._resets_password.is_valid)


class ChangeUserPasswordTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = Mock()

        self._change_password = ChangeUserPassword(user_repository=self._user_repository)

    def test_should_is_valid_false_when_old_password_is_wrong(self):
        self._user_repository.get_by_email.return_value = User(email='captain@marvel.com',
                                                               password='test12356')

        command = ChangeUserPasswordCommand(email='captain@marvel.com',
                                            old_password='test123567',
                                            new_password='test654321')

        self._change_password.execute(command)

        self.assertFalse(self._change_password.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.get_by_email.return_value = None

        command = ChangeUserPasswordCommand(email='captain@marvel.com',
                                            old_password='test12356',
                                            new_password='test654321')

        self._change_password.execute(command)

        self.assertFalse(self._change_password.is_valid)

    def test_should_ensure_add_user(self):
        self._user_repository.find_by_email.return_value = User(email='captain@marvel.com',
                                                                password='test12356')

        command = ChangeUserPasswordCommand(email='captain@marvel.com',
                                            old_password='test12356',
                                            new_password='test654321')

        self._change_password.execute(command)

        self._user_repository.add.assert_called_once()
