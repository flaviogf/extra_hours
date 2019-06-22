import unittest

from extra_hours.account.value_objects import Email, Password


class EmailTests(unittest.TestCase):
    def test_should_is_valid_true_when_email_is_valid(self):
        email = Email('naruto@hokage.com')

        self.assertTrue(email.is_valid)

    def test_should_return_is_valid_false_when_email_not_is_valid(self):
        email = Email('naruto@email')

        self.assertFalse(email.is_valid)


class PasswordTests(unittest.TestCase):
    def test_should_return_is_valid_true_when_password_is_valid(self):
        password = Password('sasuke123')

        self.assertTrue(password.is_valid)

    def test_should_return_is_valid_false_when_password_not_contains_min_len_6(self):
        password = Password('sas12')

        self.assertFalse(password.is_valid)

    def test_should_return_is_valid_false_when_password_not_contains_alphabetic_character(self):
        password = Password('123456')

        self.assertFalse(password.is_valid)

    def test_should_return_is_valid_false_when_password_not_contains_numeric_character(self):
        password = Password('sasuke uchiha')

        self.assertFalse(password.is_valid)

    def test_should_encrypt_password_when_encrypt_is_true(self):
        password = Password('sasuke123')

        self.assertNotEqual('sasuke123', str(password))

    def test_should_not_encrypt_password_when_encrypt_is_false(self):
        password = Password('sasuke123', encrypt=False)

        self.assertEqual('sasuke123', str(password))
