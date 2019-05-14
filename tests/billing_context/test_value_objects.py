import unittest
from datetime import datetime

from extra_hours.billing_context.value_objects import BillingSummary


class BillingSummaryTests(unittest.TestCase):
    def test_should_is_valid_true_when_all_information_is_valid(self):
        summary = BillingSummary(title='Gas stations',
                                 description='Gas station security yesterday',
                                 value=100.50)

        self.assertEqual('Gas stations', summary.title)
        self.assertEqual('Gas station security yesterday', summary.description)
        self.assertEqual(100.50, summary.value)
        self.assertTrue(summary.is_valid)

    def test_should_is_valid_false_when_title_not_has_min_len_3(self):
        summary = BillingSummary(title='',
                                 description='Gas station security yesterday',
                                 value=100.50)

        self.assertFalse(summary.is_valid)

    def test_should_is_valid_false_when_description_not_has_min_len_3(self):
        summary = BillingSummary(title='Gas station security',
                                 description='',
                                 value=100.50)

        self.assertFalse(summary.is_valid)

    def test_should_is_valid_false_when_value_is_not_greater_than_0(self):
        summary = BillingSummary(title='Gas station security',
                                 description='Gas station security yesterday',
                                 value=0)

        self.assertFalse(summary.is_valid)

    def test_should_work_date_equal_to_today_when_not_work_date_not_is_informed(self):
        summary = BillingSummary(title='Gas station security',
                                 description='Gas station security yesterday',
                                 value=0)

        self.assertEqual(datetime.now().date(), summary.work_date.date())
