import unittest

from firebase_admin.auth import list_users, delete_user

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository


class FirebaseUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        self._steve = User(email='captain@marvel.com',
                           password='test123456')

        self._user_repository = FirebaseUserRepository()

    def test_should_check_email(self):
        email_available = self._user_repository.check_email('captain@marvel.com')

        self.assertTrue(email_available)

    def test_should_save_user_create_user_when_user_not_exists(self):
        self._user_repository.save(self._steve)

        users = list(list_users().iterate_all())

        self.assertEqual(1, len(users))

    def tearDown(self):
        self._delete_all_users()

    def _delete_all_users(self):
        for user in list_users().iterate_all():
            delete_user(user.uid)
