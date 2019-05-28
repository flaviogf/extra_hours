import uuid
from datetime import datetime

from firebase_admin import firestore
from firebase_admin.auth import create_user, delete_user, list_users

from extra_hours.billing.entities import Billing, User
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.billing.value_objects import BillingSummary
from tests.billing.gateways.infra.base import InfraTestCase


class FirebaseUserRepositoryTests(InfraTestCase):
    def setUp(self):
        self._steve_id = uuid.uuid4()

        self._steve = User(uid=self._steve_id)

        self._yesterday = datetime(year=2019, month=6, day=13)

        self._billing_summary = BillingSummary(title='Gas station security',
                                               description='Gas station security yesterday',
                                               value=100.50,
                                               work_date=self._yesterday)

        self._billing = Billing(summary=self._billing_summary)

        create_user(uid=str(self._steve.uid), email='steve@email.com', password='test123')

        self._user_repository = FirebaseUserRepository()

    def test_should_find_by_id_return_use_when_user_exists(self):
        user = self._user_repository.find_by_id(self._steve_id)

        self.assertIsInstance(user, User)

    def test_should_find_by_id_return_none_when_user_not_exists(self):
        user = self._user_repository.find_by_id(uuid.uuid4())

        self.assertIsNone(user)

    def test_should_save_user(self):
        self._steve.add_billing(self._billing)

        self._user_repository.save(self._steve)

    def tearDown(self):
        self._delete_user()
        self._delete_user_document()

    def _delete_user(self):
        for user in list_users().iterate_all():
            delete_user(user.uid)

    def _delete_user_document(self):
        db = firestore.client()

        user_collection = db.collection('user')

        for user in user_collection.list_documents():

            for billing in user.collection('billing').list_documents():
                billing.delete()

            user.delete()
