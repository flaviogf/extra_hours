import unittest

from extra_hours.account.value_objects import Password, Email


class PasswordTests(unittest.TestCase):
    def test_should_is_valid_true_when_password_contains_min_len_6_and_alphabetic_and_numeric_characters(self):
        password = Password(password='test123456')

        self.assertTrue(password.is_valid)

    def test_should_is_valid_false_when_password_not_has_min_len_6(self):
        password = Password(password='test')

        self.assertFalse(password.is_valid)

    def test_should_is_valid_false_when_password_not_has_alphabetic_character(self):
        password = Password(password='111111')

        self.assertFalse(password.is_valid)

    def test_should_is_valid_false_when_password_not_has_numeric_character(self):
        password = Password(password='test test test')

        self.assertFalse(password.is_valid)

    def test_should_str_return_raw_password(self):
        password = Password(password='test123456')

        self.assertEqual('test123456', str(password))


class EmailTests(unittest.TestCase):
    def test_should_is_valid_true_when_email_is_valid(self):
        email = Email(email='captain@marvel.com')

        self.assertTrue(email.is_valid)

    def test_should_is_valid_false_when_email_not_is_valid(self):
        email = Email(email='captain')

        self.assertFalse(email.is_valid)

    def test_should_str_return_raw_email(self):
        email = Email(email='captain@marvel.com')

        self.assertEqual('captain@marvel.com', str(email))
