import unittest

from firebase_admin.auth import list_users, delete_user

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository


class FirebaseUserRepositoryTests(unittest.TestCase):
    def test_should_save_user(self):
        steve = User(email='captain@marvel.com',
                     password='test123456')

        user_repository = FirebaseUserRepository()

        user_repository.save(steve)

    def tearDown(self):
        self._delete_all_users()

    def _delete_all_users(self):
        for user in list_users().iterate_all():
            delete_user(user.uid)
