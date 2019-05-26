import unittest
import uuid

from extra_hours.billing.entities import User
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository


class FirebaseUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        self._steve_id = uuid.uuid4()

        self._steve = User(uid=self._steve_id)

        self._user_repository = FirebaseUserRepository()

    def test_should_find_by_id_return_use_when_user_exists(self):
        user = self._user_repository.find_by_id(self._steve_id)

        self.assertIsInstance(user, User)

    def test_should_save_user(self):
        self._user_repository.save(self._steve)
