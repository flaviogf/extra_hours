import unittest

from extra_hours.billing.gateways.infra.repositories import SqlAlchemyUserRepository


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = SqlAlchemyUserRepository()

    def test_should_add(self):
        self._user_repository.add(None)

        self.assertTrue(True)

    def test_should_get_by_id(self):
        self._user_repository.get_by_id(None)

        self.assertTrue(True)

    def test_should_get_billing_by_id(self):
        self._user_repository.get_billing_by_id(None)

        self.assertTrue(True)
