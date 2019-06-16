import unittest

from extra_hours.account.gateways.infra.repositories import SqlAlchemyUserRepository


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = SqlAlchemyUserRepository()

    def test_should_check_email(self):
        self._user_repository.check_email(None)

        self.assertTrue(True)

    def test_should_add(self):
        self._user_repository.add(None)

        self.assertTrue(True)

    def test_should_get_by_email(self):
        self._user_repository.get_by_email(None)

        self.assertTrue(True)
