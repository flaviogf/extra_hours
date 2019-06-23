import unittest
from unittest.mock import Mock

from extra_hours.account.commands import CreateUserCommand, AuthenticateUserCommand
from extra_hours.account.entities import User
from extra_hours.account.use_cases import CreateUser, AuthenticateUser
from extra_hours.account.value_objects import Email, Password


class CreateUserTests(unittest.TestCase):
    def test_should_is_valid_true_when_user_created_is_valid(self):
        user_repository = Mock()

        use_case = CreateUser(user_repository)

        command = CreateUserCommand(email='naruto@uzumaki.com', password='sasuke123')

        use_case.execute(command)

        self.assertTrue(use_case.is_valid)

    def test_should_is_valid_false_when_user_created_not_is_valid(self):
        user_repository = Mock()

        use_case = CreateUser(user_repository)

        command = CreateUserCommand(email='naruto@uzumaki.com', password='sas')

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)

    def test_should_is_valid_false_when_email_not_is_available(self):
        user_repository = Mock()

        user_repository.check_email.return_value = False

        use_case = CreateUser(user_repository)

        command = CreateUserCommand(email='naruto@uzumaki.com', password='sasuke123')

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)


class AuthenticateUserTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = Mock()
        self._token_service = Mock()

        self._use_case = AuthenticateUser(self._user_repository, self._token_service)

    def test_should_is_valid_true_when_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        self._user_repository.get_by_email.return_value = naruto

        command = AuthenticateUserCommand(email='naruto@uzumaki.com', password='sasuke123')

        self._use_case.execute(command)

        self.assertTrue(self._use_case.is_valid)

    def test_should_return_token_when_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        self._user_repository.get_by_email.return_value = naruto

        self._token_service.encode.return_value = 'token'

        command = AuthenticateUserCommand(email='naruto@uzumaki.com', password='sasuke123')

        token = self._use_case.execute(command)

        self.assertEqual('token', token)

    def test_should_is_valid_false_when_not_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        self._user_repository.get_by_email.return_value = naruto

        command = AuthenticateUserCommand(email='naruto@uzumaki.com', password='sasuke321')

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.get_by_email.return_value = None

        command = AuthenticateUserCommand(email='naruto@uzumaki.com', password='sasuke321')

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)

    def test_should_return_none_when_not_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        self._user_repository.get_by_email.return_value = naruto

        self._token_service.encode.return_value = None

        command = AuthenticateUserCommand(email='naruto@uzumaki.com', password='sasuke321')

        token = self._use_case.execute(command)

        self.assertEqual(token, None)
