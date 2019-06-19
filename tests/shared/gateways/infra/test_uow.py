import unittest
import uuid
from datetime import datetime
from unittest.mock import Mock

from extra_hours.shared.gateways.infra.uow import UserTable, Uow, BillingTable


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
    def test_should_return_repr_string(self):
        uid = str(uuid.uuid4())

        naruto = UserTable(uid=uid, email='peter@marvel.com', password='test123')

        result = repr(naruto)

        expected = f"<User(uid='{uid}', email='peter@marvel.com')>"

        self.assertEqual(expected, result)


class BillingTableTests(unittest.TestCase):
    def test_should_return_repr_string(self):
        uid = str(uuid.uuid4())

        user_uid = str(uuid.uuid4())

        billing = BillingTable(uid=uid,
                               title='Gas Station',
                               description='Yesterday',
                               value=100.99,
                               work_date=datetime.now(),
                               user_uid=user_uid)

        result = repr(billing)

        expected = f"<Billing(uid='{uid}', title='Gas Station', value=100.99)>"

        self.assertEqual(expected, result)

    def test_should_equal_when_uid_are_equal(self):
        uid = str(uuid.uuid4())

        user_uid = str(uuid.uuid4())

        billing_1 = BillingTable(uid=uid,
                                 title='Gas Station',
                                 description='Yesterday',
                                 value=100.99,
                                 work_date=datetime.now(),
                                 user_uid=user_uid)

        billing_2 = BillingTable(uid=uid,
                                 title='Gas Station',
                                 description='Yesterday',
                                 value=100.99,
                                 work_date=datetime.now(),
                                 user_uid=user_uid)

        self.assertEqual(billing_1, billing_2)
