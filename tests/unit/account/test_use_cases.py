import unittest
from unittest.mock import Mock

from extra_hours.account.commands import CreateUserCommand
from extra_hours.account.use_cases import CreateUser


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
