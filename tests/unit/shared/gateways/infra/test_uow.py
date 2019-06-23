import unittest
import uuid
from decimal import Decimal
from unittest.mock import Mock

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from extra_hours.shared.gateways.infra.uow import Uow, UserTable, BillingTable


class UowTests(unittest.TestCase):
    def setUp(self):
        self._uow = Uow('sqlite:///:memory:')

    def test_should_uow_initialize_a_session(self):
        self.assertIsInstance(self._uow.session, Session)

    def test_should_uow_commit_when_not_raise_a_error(self):
        session = Mock()

        self._uow._session = session

        with self._uow():
            pass

        session.commit.assert_called()

    def test_should_uow_rollback_when_raise_a_error(self):
        session = Mock()

        self._uow._session = session

        with self._uow():
            raise Exception()

        session.rollback.assert_called()


class UserTableTests(unittest.TestCase):
    def test_should_return_str_repr(self):
        naruto = UserTable(uid=str(uuid.uuid4()), email='naruto@uzumaki', password='sasuke123')

        expected = f"<User(uid='{naruto.uid}', email='{naruto.email}')>"

        result = str(naruto)

        self.assertEqual(expected, result)


class BillingTableTests(unittest.TestCase):
    def test_should_return_str_repr(self):
        yesterday = datetime.now() - timedelta(days=1)

        billing = BillingTable(uid=str(uuid.uuid4()),
                               title='Gas Station',
                               description='Yesterday',
                               value=Decimal(10),
                               work_date=yesterday)

        result = repr(billing)

        expected = f"<Billing(uid='{billing.uid}', received={billing.received})>"

        self.assertEqual(expected, result)
