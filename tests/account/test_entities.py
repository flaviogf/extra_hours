import unittest

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Password, Email


class UserTests(unittest.TestCase):
    def test_should_is_valid_true_when_all_information_is_valid(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        self.assertTrue(user.is_valid)

    def test_should_is_valid_false_when_email_not_is_valid(self):
        password = Password('test123567')
        email = Email('captain')

        user = User(email=email,
                    password=password)

        self.assertFalse(user.is_valid)

    def test_should_is_valid_false_when_password_not_is_valid(self):
        password = Password('test test test')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        self.assertFalse(user.is_valid)

    def test_should_resets_password(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        user.resets_password()

        self.assertNotEqual(password, user._password)

    def test_should_is_valid_true_when_resets_password(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        user.resets_password()

        self.assertTrue(user.is_valid)

    def test_should_change_password(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        new_password = Password('test45678')

        user.change_password(new_password)

        self.assertNotEqual(password, user._password)

    def test_should_is_valid_true_when_change_password_valid(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        new_password = Password('test45678')

        user.change_password(new_password)

        self.assertTrue(user.is_valid)

    def test_should_is_valid_false_when_change_password_invalid(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email,
                    password=password)

        new_password = Password('test')

        user.change_password(new_password)

        self.assertFalse(user.is_valid)
