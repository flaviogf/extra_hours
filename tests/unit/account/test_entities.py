import unittest

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password


class UserTests(unittest.TestCase):
    def test_should_is_valid_true_when_email_and_password_is_valid(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        self.assertTrue(naruto.is_valid)

    def test_should_is_valid_false_when_email_not_is_valid(self):
        email = Email('naruto')
        password = Password('sasuke123')

        naruto = User(email, password)

        self.assertFalse(naruto.is_valid)

    def test_should_is_valid_false_when_password_not_is_valid(self):
        email = Email('naruto@hokage.com')
        password = Password('sas')

        naruto = User(email, password)

        self.assertFalse(naruto.is_valid)

    def test_should_is_valid_true_when_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        naruto.authenticate(Password('sasuke123'))

        self.assertTrue(naruto.is_valid)

    def test_should_is_valid_false_when_not_authenticate(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        naruto.authenticate(Password('sasuke321'))

        self.assertFalse(naruto.is_valid)

    def test_should_change_password_when_old_password_is_right(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        new_password = Password('boruto123')

        naruto.change_password(old_password=password, new_password=new_password)

        self.assertEqual(naruto.password, str(new_password))

    def test_should_not_change_password_when_old_password_is_wrong(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        wrong_password = Password('sakura123')

        new_password = Password('boruto123')

        naruto.change_password(old_password=wrong_password, new_password=new_password)

        self.assertEqual(naruto.password, str(password))

    def test_should_is_valid_false_when_old_password_is_wrong(self):
        email = Email('naruto@hokage.com')
        password = Password('sasuke123')

        naruto = User(email, password)

        wrong_password = Password('sakura123')

        new_password = Password('boruto123')

        naruto.change_password(old_password=wrong_password, new_password=new_password)

        self.assertFalse(naruto.is_valid)
