import unittest

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Password, Email


class UserTests(unittest.TestCase):
    def test_should_is_valid_true_when_all_information_is_valid(self):
        password = Password('test123567')
        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        self.assertTrue(user.is_valid)

    def test_should_is_valid_false_when_email_not_is_valid(self):
        password = Password('test123567')
        email = Email('captain')

        user = User(email=email, password=password)

        self.assertFalse(user.is_valid)

    def test_should_is_valid_false_when_password_not_is_valid(self):
        password = Password('test test test')
        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        self.assertFalse(user.is_valid)

    def test_should_resets_password(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        user.resets_password()

        self.assertNotEqual(password, user._password)

    def test_should_is_valid_true_when_resets_password(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        user.resets_password()

        self.assertTrue(user.is_valid)

    def test_should_change_password_when_old_password_is_correct(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        old_password = Password('test123567')

        new_password = Password('test45678')

        user.change_password(old_password, new_password)

        self.assertEqual(new_password, user._password)

    def test_should_not_change_password_when_old_password_not_is_correct(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        new_password = Password('test45678')

        old_password = Password('test12356')

        user.change_password(old_password, new_password)

        self.assertEqual(password, user._password)

    def test_should_is_valid_true_when_new_password_is_valid(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        old_password = Password('test123567')

        new_password = Password('test45678')

        user.change_password(old_password, new_password)

        self.assertTrue(user.is_valid)

    def test_should_is_valid_false_when_new_password_not_is_valid(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        new_password = Password('test45678')

        old_password = Password('test12356')

        user.change_password(old_password, new_password)

        self.assertFalse(user.is_valid)

    def test_should_to_dict_return_user_dict_representation(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        expected = {
            'uid': str(user.uid),
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        self.assertDictEqual(expected, user.to_dict())

    def test_should_is_valid_true_when_authenticate(self):
        password = Password('test123567')

        email = Email('captain@marvel.com.br')

        user = User(email=email, password=password)

        user.authenticate(password=Password('test123567'))

        self.assertTrue(user.is_valid)
