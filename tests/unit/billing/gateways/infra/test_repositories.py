import unittest
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from extra_hours.billing.entities import Billing, User
from extra_hours.billing.gateways.infra.repositories import SqlAlchemyUserRepository
from extra_hours.billing.queries import BillingListQueryResult
from extra_hours.shared.gateways.infra.uow import BillingTable, Base, UserTable


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

        uow = Mock()
        uow.session = self._session

        self._user_repository = SqlAlchemyUserRepository(uow)

    def test_should_save_billing_create_billing_when_not_exists(self):
        yesterday = datetime.now() + timedelta(days=1)

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        naruto = User()

        self._user_repository.save_billing(naruto, billing)

        result = len(self._session.query(BillingTable).all())

        expected = 1

        self.assertEqual(expected, result)

    def test_should_save_billing_update_billing_when_exists(self):
        yesterday = datetime.now() + timedelta(days=1)

        billing_table = BillingTable(uid=str(uuid.uuid4()),
                                     title='Gas Station',
                                     description='Yesterday',
                                     value=Decimal(10),
                                     work_date=yesterday)

        self._session.add(billing_table)

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday,
                          uid=billing_table.uid)

        naruto = User()

        self._user_repository.save_billing(naruto, billing)

        result = len(self._session.query(BillingTable).all())

        expected = 1

        self.assertEqual(expected, result)

    def test_should_get_by_uid_return_user_when_user_exists(self):
        user_uid = str(uuid.uuid4())

        user_table = UserTable(uid=user_uid)

        self._session.add(user_table)

        user = self._user_repository.get_by_uid(user_uid)

        self.assertIsInstance(user, User)

    def test_should_get_by_uid_return_none_when_user_not_exists(self):
        user_uid = str(uuid.uuid4())

        user = self._user_repository.get_by_uid(user_uid)

        self.assertIsNone(user)

    def test_should_get_billing_by_uid_return_billing_when_user_exists(self):
        billing_uid = str(uuid.uuid4())

        billing_table = BillingTable(uid=billing_uid,
                                     title='',
                                     description='',
                                     value=Decimal(10),
                                     work_date=datetime.now())

        self._session.add(billing_table)

        billing = self._user_repository.get_billing_by_uid(billing_uid)

        self.assertIsInstance(billing, Billing)

    def test_should_get_billing_by_uid_return_none_when_user_not_exists(self):
        billing_uid = str(uuid.uuid4())

        billing = self._user_repository.get_billing_by_uid(billing_uid)

        self.assertIsNone(billing)

    def test_should_list_billing_received_return_only_billing_received(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_received(user_uid)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_received_return_default_limit_and_offset_when_not_inform_limit_and_offset(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_received(user_uid)

        self.assertEqual(2, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_received_return_a_billing_when_limit_is_equal_to_one(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_received(user_uid, limit=1)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_received_return_second_billing_when_offset_is_equal_to_one(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_received(user_uid, offset=1)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_not_received_return_only_billing_received(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       receive_date=datetime.now(),
                                       received=True,
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_not_received(user_uid)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_not_received_return_default_limit_and_offset_when_not_inform_limit_and_offset(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_not_received(user_uid)

        self.assertEqual(2, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_not_received_return_a_billing_when_limit_is_equal_to_one(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_not_received(user_uid, limit=1)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)

    def test_should_list_billing_not_received_return_second_billing_when_offset_is_equal_to_one(self):
        user_uid = str(uuid.uuid4())

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        self._session.add(BillingTable(uid=str(uuid.uuid4()),
                                       title='',
                                       description='',
                                       value=Decimal(10),
                                       work_date=datetime.now(),
                                       user_uid=user_uid))

        billing_received = self._user_repository.list_billing_not_received(user_uid, offset=1)

        self.assertEqual(1, len(billing_received))

        for it in billing_received:
            with self.subTest():
                self.assertIsInstance(it, BillingListQueryResult)
