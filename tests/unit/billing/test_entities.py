import unittest
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from extra_hours.billing.entities import Billing, User

yesterday = datetime.now() - timedelta(days=1)


class UserTests(unittest.TestCase):
    def test_should_add_billing(self):
        naruto = User(uid=str(uuid.uuid4()))

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        naruto.add_billing(billing)

        self.assertEqual(1, len(naruto.billing))

    def test_should_confirm_receive_billing_confirm_receive(self):
        naruto = User(uid=str(uuid.uuid4()))

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        naruto.confirm_receive_billing(billing)

        self.assertIsInstance(billing.receive_date, datetime)

    def test_should_cancel_receive_billing_cancel_receive(self):
        naruto = User(uid=str(uuid.uuid4()))

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        naruto.confirm_receive_billing(billing)

        naruto.cancel_receive_billing(billing)

        self.assertIsNone(billing.receive_date)


class BillingTests(unittest.TestCase):
    def test_should_is_valid_false_when_receive_date_is_lower_than_work_date(self):
        before_yesterday = yesterday - timedelta(days=1)

        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday,
                          receive_date=before_yesterday)

        self.assertFalse(billing.is_valid)

    def test_should_receive_date_is_none_when_receive_date_not_is_inform(self):
        billing = Billing(title='',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        self.assertIsNone(billing.receive_date)

    def test_should_received_is_false_when_receive_date_not_is_inform(self):
        billing = Billing(title='',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        self.assertFalse(billing.received)

    def test_should_is_valid_false_when_title_is_empty_or_none(self):
        billing = Billing(title='',
                          description='Yesterday',
                          value=Decimal(10),
                          work_date=yesterday)

        self.assertFalse(billing.is_valid)

    def test_should_is_valid_false_when_description_is_empty_or_none(self):
        billing = Billing(title='Gas Station',
                          description='',
                          value=Decimal(10),
                          work_date=yesterday)

        self.assertFalse(billing.is_valid)

    def test_should_is_valid_false_when_value_is_negative(self):
        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(-10),
                          work_date=yesterday)

        self.assertFalse(billing.is_valid)

    def test_should_confirm_receive_update_received_date(self):
        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(-10),
                          work_date=yesterday)

        billing.confirm_receive()

        self.assertIsInstance(billing.receive_date, datetime)

    def test_should_cancel_receive_update_received_date_to_none(self):
        billing = Billing(title='Gas Station',
                          description='Yesterday',
                          value=Decimal(-10),
                          work_date=yesterday)

        billing.confirm_receive()

        billing.cancel_receive()

        self.assertIsNone(billing.receive_date)
