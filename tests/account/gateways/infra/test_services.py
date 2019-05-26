import uuid

from firebase_admin.auth import create_user, list_users, delete_user

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.services import FirebaseUserService
from tests.account.gateways.infra.base import InfraTestCase


class FirebaseUserServiceTests(InfraTestCase):
    def setUp(self):
        create_user(email='captain@marvel.com', password='test12345', uid=str(uuid.uuid4()))

    def test_should_return_user_when_user_authenticated(self):
        user_service = FirebaseUserService()

        user, _ = user_service.sign_with_email_and_password(email='captain@marvel.com', password='test12345')

        self.assertIsInstance(user, User)

    def test_should_return_token_when_user_authenticated(self):
        user_service = FirebaseUserService()

        _, token = user_service.sign_with_email_and_password(email='captain@marvel.com', password='test12345')

        self.assertIsInstance(token, str)

    def test_should_return_tuple_of_none_when_user_not_authenticated(self):
        user_service = FirebaseUserService()

        user, token = user_service.sign_with_email_and_password(email='flavio.fernandes@gmail.com',
                                                                password='test12345')

        self.assertIsNone(user)
        self.assertIsNone(token)

    def tearDown(self):
        self._delete_all_users()

    def _delete_all_users(self):
        for user in list_users().iterate_all():
            delete_user(user.uid)
