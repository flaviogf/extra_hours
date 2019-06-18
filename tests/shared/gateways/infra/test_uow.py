import unittest
import uuid
from unittest.mock import Mock

from extra_hours.shared.gateways.infra.uow import UserTable, Uow


class UowTests(unittest.TestCase):
    def setUp(self):
        self._uow = Uow(connection_string='sqlite:///:memory:')

    def test_should_uow_create_a_session(self):
        self.assertIsNotNone(self._uow.session)

    def test_should_exit_call_commit_when_not_raise_exception(self):
        session = Mock()

        self._uow._session = session

        with self._uow():
            pass

        session.commit.assert_called_once()

    def test_should_exit_call_commit_when_raise_exception(self):
        session = Mock()

        self._uow._session = session

        with self._uow():
            raise ValueError()

        session.rollback.assert_called_once()


class UserTableTests(unittest.TestCase):
    def test_should_repr(self):
        naruto = UserTable(uid=str(uuid.uuid4()), email='peter@marvel.com', password='test123')

        result = repr(naruto)

        expected = "<User(email='peter@marvel.com')>"

        self.assertEqual(expected, result)
