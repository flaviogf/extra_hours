import unittest
import uuid
from datetime import datetime

from extra_hours.billing.entities import Billing, User
from extra_hours.billing.value_objects import BillingSummary


class BillingTests(unittest.TestCase):
    def setUp(self):
        self._yesterday = datetime(year=2019, month=6, day=13)

        self._billing_summary = BillingSummary(title='Gas station security',
                                               description='Gas station security yesterday',
                                               value=100.50,
                                               work_date=self._yesterday)

        self._billing = Billing(summary=self._billing_summary)

    def test_should_create_billing_when_all_information_is_valid(self):
        self.assertEqual('Gas station security', self._billing.title)
        self.assertEqual('Gas station security yesterday', self._billing.description)
        self.assertEqual(100.50, self._billing.value)
        self.assertEqual(self._yesterday, self._billing.work_date)
        self.assertTrue(self._billing.is_valid)

    def test_should_is_valid_false_when_summary_not_is_valid(self):
        billing_summary = BillingSummary(title='',
                                         description='Gas station security yesterday',
                                         value=100.50)

        billing = Billing(summary=billing_summary)

        self.assertFalse(billing.is_valid)

    def test_should_work_date_equal_to_today_when_billing_is_created_without_work_date(self):
        billing_summary = BillingSummary(title='Gas station security',
                                         description='Gas station security yesterday',
                                         value=100.50)

        billing = Billing(summary=billing_summary)

        self.assertEqual(datetime.now().date(), billing.work_date.date())

    def test_should_receive_date_is_none_when_billing_is_created(self):
        self.assertIsNone(self._billing.received_date)

    def test_should_received_false_when_billing_is_created(self):
        self.assertFalse(self._billing.received)

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

    def test_should_is_valid_true_when_update_summary_with_summary_updated_valid(self):
        summary_updated = BillingSummary(title='Gym',
                                         description='Tomorrow',
                                         value=50)

        self._billing.update_summary(summary_updated)

        self.assertEqual('Gym', self._billing.title)
        self.assertEqual('Tomorrow', self._billing.description)
        self.assertEqual(50, self._billing.value)
        self.assertTrue(self._billing.is_valid)

    def test_should_is_valid_false_when_update_summary_with_summary_updated_not_valid(self):
        summary_updated = BillingSummary(title='',
                                         description='Tomorrow',
                                         value=50)

        self._billing.update_summary(summary_updated)

        self.assertFalse(self._billing.is_valid)

    def test_should_to_dict_return_all_billing_properties(self):
        self._billing.confirm_receive()

        expected = {
            'title': self._billing.title,
            'description': self._billing.description,
            'value': self._billing.value,
            'work_date': self._billing.work_date.strftime('%Y-%m-%d'),
            'received_date': self._billing.received_date.strftime('%Y-%m-%d'),
            'received': self._billing.received,
        }

        self.assertDictEqual(expected, self._billing.to_dict())


class UserTests(unittest.TestCase):
    def setUp(self):
        self._uid = uuid.uuid4()

        yesterday = datetime(year=2019, month=6, day=13)

        self._billing_summary = BillingSummary(title='Gas station security',
                                               description='Gas station security yesterday',
                                               value=100.50,
                                               work_date=yesterday)

        self._billing = Billing(summary=self._billing_summary)

        self._batman = User(uid=self._uid)

    def test_should_create_user_when_all_information_is_valid(self):
        self.assertTrue(self._batman.is_valid)

    def test_should_billing_is_empty_list_when_user_is_created(self):
        self.assertTupleEqual((), self._batman.billing)

    def test_should_billing_received_is_empty_list_when_user_is_created(self):
        self.assertTupleEqual((), self._batman.billing_received)

    def test_should_billing_not_received_is_empty_list_when_user_is_created(self):
        self.assertTupleEqual((), self._batman.billing_not_received)

    def test_should_billing_in_billing_when_add_billing(self):
        self._batman.add_billing(self._billing)

        self.assertTrue(self._billing in self._batman.billing)

    def test_should_billing_in_billing_received_list_when_confirm_receive(self):
        self._batman.add_billing(self._billing)

        self._batman.confirm_receive(self._billing)

        self.assertTrue(self._billing in self._batman.billing_received)

    def test_should_not_confirm_receive_billing_when_billing_not_in_billing_list(self):
        self._batman.confirm_receive(self._billing)

        self.assertFalse(self._billing.received)

    def test_should_all_billing_in_billing_received_list_are_received(self):
        self._batman.add_billing(self._billing)

        self._batman.confirm_receive(self._billing)

        with self.subTest():
            for billing in self._batman.billing_received:
                self.assertTrue(billing.received)

    def test_should_billing_in_billing_not_received_list_when_cancel_receive(self):
        self._batman.add_billing(self._billing)

        self._batman.confirm_receive(self._billing)

        self._batman.cancel_receive(self._billing)

        self.assertTrue(self._billing in self._batman.billing_not_received)

    def test_should_not_cancel_receive_billing_when_billing_not_in_billing_list(self):
        self._billing.confirm_receive()

        self._batman.cancel_receive(self._billing)

        self.assertTrue(self._billing.received)

    def test_should_all_billing_in_billing_not_received_list_are_not_received(self):
        self._batman.add_billing(self._billing)

        self._batman.confirm_receive(self._billing)

        self._batman.cancel_receive(self._billing)

        with self.subTest():
            for billing in self._batman.billing_not_received:
                self.assertFalse(billing.received)

    def test_should_update_billing_summary_when_billing_in_billing_list(self):
        self._batman.add_billing(self._billing)

        before_yesterday = datetime(2019, 1, 10)

        summary_updated = BillingSummary(title='Gym',
                                         description='Tomorrow',
                                         value=100,
                                         work_date=before_yesterday)

        self._batman.update_billing_summary(self._billing, summary_updated)

        self.assertEqual('Gym', self._billing.title)

    def test_should_not_update_billing_summary_when_billing_not_in_billing_list(self):
        before_yesterday = datetime(2019, 1, 10)

        summary_updated = BillingSummary(title='Gym',
                                         description='Tomorrow',
                                         value=100,
                                         work_date=before_yesterday)

        self._batman.update_billing_summary(self._billing, summary_updated)

        self.assertEqual('Gas station security', self._billing.title)
