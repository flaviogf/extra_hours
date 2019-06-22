import unittest

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password


class UserTests(unittest.TestCase):
    def test_should_return_is_valid_true_when_email_and_password_is_valid(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        self.assertTrue(naruto.is_valid)

    def test_should_return_is_valid_false_when_email_not_is_valid(self):
        email = Email('naruto')
        password = Password('sasuke123')

        naruto = User(email, password)

        self.assertFalse(naruto.is_valid)

    def test_should_return_is_valid_false_when_password_not_is_valid(self):
        email = Email('naruto@hokage.com')
        password = Password('sas')

        naruto = User(email, password)

        self.assertFalse(naruto.is_valid)
