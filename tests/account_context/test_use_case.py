import unittest
from unittest.mock import Mock

from extra_hours.account_context.commands import CreateUserCommand
from extra_hours.account_context.use_case import CreateUser


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
