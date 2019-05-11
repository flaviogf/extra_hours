import unittest
from datetime import datetime

from extra_hours.billing_context.entities import Billing


class BillingTests(unittest.TestCase):
    def setUp(self):
        self._yesterday = datetime(year=2019, month=6, day=13)

        self._billing = Billing(title='Gas station security',
                                description='Gas station security yesterday',
                                value=100.50,
                                work_date=self._yesterday)

    def test_should_create_billing_when_all_information_is_valid(self):
        self.assertEqual('Gas station security', self._billing.title)
        self.assertEqual('Gas station security yesterday', self._billing.description)
        self.assertEqual(100.50, self._billing.value)
        self.assertEqual(self._yesterday, self._billing.work_date)
        self.assertTrue(self._billing.is_valid)

    def test_should_work_date_equal_to_today_when_billing_is_created_without_work_date(self):
        billing = Billing(title='Gas station security',
                          description='Gas station security yesterday',
                          value=100.50)

        self.assertEqual(datetime.now().date(), billing.work_date.date())

    def test_should_receive_date_is_none_when_billing_is_created(self):
        self.assertIsNone(self._billing.received_date)

    def test_should_received_false_when_billing_is_created(self):
        self.assertFalse(self._billing.received)

    def test_should_is_valid_false_when_title_not_has_min_len_3(self):
        billing = Billing(title='',
                          description='Gas station security yesterday',
                          value=100.50)

        self.assertFalse(billing.is_valid)

    def test_should_is_valid_false_when_description_not_has_min_len_3(self):
        billing = Billing(title='Gas station security',
                          description='',
                          value=100.50)

        self.assertFalse(billing.is_valid)

    def test_should_is_valid_false_when_value_is_not_greater_than_0(self):
        billing = Billing(title='Gas station security',
                          description='Gas station security yesterday',
                          value=0)

        self.assertFalse(billing.is_valid)

    def test_should_received_date_equal_to_date_today_when_confirm_receive(self):
        self._billing.confirm_receive()

        self.assertEqual(datetime.now().date(), self._billing.received_date.date())

    def test_should_received_true_when_confirm_receive(self):
        self._billing.confirm_receive()

        self.assertTrue(self._billing.received)

    def test_should_received_date_equal_to_none_when_cancel_receive(self):
        self._billing.confirm_receive()

        self._billing.cancel_receive()

        self.assertIsNone(self._billing.received_date)

    def test_should_received_false_when_cancel_receive(self):
        self._billing.confirm_receive()

        self._billing.cancel_receive()

        self.assertFalse(self._billing.received)
