from firebase_admin.auth import create_user, delete_user, list_users

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository
from tests.account.gateways.infra.base import InfraTestCase


class FirebaseUserRepositoryTests(InfraTestCase):
    def setUp(self):
        self._steve = User(email='captain@marvel.com',
                           password='test123456')

        self._user_repository = FirebaseUserRepository()

    def test_should_check_email(self):
        email_available = self._user_repository.check_email(
            'iron_man@marvel.com')

        self.assertTrue(email_available)

    def test_should_save_user_create_user_when_user_not_exists(self):
        self._user_repository.save(self._steve)

        users = list(list_users().iterate_all())

        self.assertEqual(1, len(users))

    def test_should_save_update_user_when_user_exists(self):
        create_user(**self._steve.to_dict())

        self._user_repository.save(self._steve)

        users = list(list_users().iterate_all())

        self.assertEqual(1, len(users))

    def test_should_find_by_email_return_use_when_user_exists(self):
        create_user(**self._steve.to_dict())

        user = self._user_repository.find_by_email('captain@marvel.com')

        self.assertIsInstance(user, User)

    def test_should_find_by_email_return_none_when_user_not_exists(self):
        user = self._user_repository.find_by_email('captain@marvel.com')

        self.assertIsNone(user)

    def tearDown(self):
        self._delete_all_users()

    def _delete_all_users(self):
        for user in list_users().iterate_all():
            delete_user(user.uid)
