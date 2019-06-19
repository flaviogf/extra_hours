import unittest
import uuid
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from extra_hours.billing.entities import User, Billing
from extra_hours.billing.gateways.infra.repositories import SqlAlchemyUserRepository
from extra_hours.billing.value_objects import BillingSummary
from extra_hours.shared.gateways.infra.uow import UserTable, BillingTable, Base


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self._session = Session()

        self._user_repository = SqlAlchemyUserRepository(self._session)

    def test_should_add_create_a_billing_when_not_exists(self):
        user_uid = str(uuid.uuid4())

        user_table = UserTable(uid=user_uid, email='naruto@uzumaki.com', password='test123')

        self._session.add(user_table)

        user = User(uid=user_uid)

        billing_uid = str(uuid.uuid4())

        summary = BillingSummary(title='Gas station', description='yesterday', value=100.99, work_date=datetime.now())

        user.add_billing(Billing(summary=summary, uid=billing_uid))

        self._user_repository.add(user)

        billing = self._session.query(BillingTable).all()

        self.assertEqual(1, len(billing))

    def test_should_add_update_a_billing_when_exists(self):
        user_uid = str(uuid.uuid4())

        user_table = UserTable(uid=user_uid, email='naruto@uzumaki.com', password='test123')

        self._session.add(user_table)

        user = User(uid=user_uid)

        billing_uid = str(uuid.uuid4())

        summary = BillingSummary(title='Gas station', description='yesterday', value=100.99, work_date=datetime.now())

        user.add_billing(Billing(summary=summary, uid=billing_uid))

        self._user_repository.add(user)
        self._user_repository.add(user)

        billing = self._session.query(BillingTable).all()

        self.assertEqual(1, len(billing))

    def test_should_get_by_id_return_user_when_exists(self):
        user_uid = str(uuid.uuid4())

        user_table = UserTable(uid=user_uid, email='naruto@uzumaki.com', password='test123')

        self._session.add(user_table)

        user = self._user_repository.get_by_id(user_uid)

        self.assertIsInstance(user, User)

    def test_should_get_by_id_return_none_when_user_not_exists(self):
        user_uid = str(uuid.uuid4())

        user = self._user_repository.get_by_id(user_uid)

        self.assertIsNone(user)

    def test_should_get_billing_by_id_return_billing_exists(self):
        user_uid = str(uuid.uuid4())

        user_table = UserTable(uid=user_uid, email='naruto@uzumaki.com', password='test123')

        self._session.add(user_table)

        user = User(uid=user_uid)

        billing_uid = str(uuid.uuid4())

        summary = BillingSummary(title='Gas station', description='yesterday', value=100.99, work_date=datetime.now())

        user.add_billing(Billing(summary=summary, uid=billing_uid))

        self._user_repository.add(user)

        billing = self._user_repository.get_billing_by_id(billing_uid)

        self.assertIsInstance(billing, Billing)

    def test_should_get_billing_by_id_return_none_when_billing_not_exists(self):
        billing_uid = str(uuid.uuid4())

        billing = self._user_repository.get_billing_by_id(billing_uid)

        self.assertIsNone(billing)
