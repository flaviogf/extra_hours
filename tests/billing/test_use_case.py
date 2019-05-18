import unittest
import uuid
from datetime import datetime
from unittest.mock import Mock

from extra_hours.billing.commands import (CreateBillingCommand,
                                          ConfirmReceiveBillingCommand,
                                          CancelReceiveBillingCommand,
                                          UpdateBillingCommand)
from extra_hours.billing.entities import User, Billing
from extra_hours.billing.use_case import (CreateBilling,
                                          ConfirmReceiveBilling,
                                          CancelReceiveBilling,
                                          UpdateBilling)
from extra_hours.billing.value_objects import BillingSummary


class CreateBillingTests(unittest.TestCase):
    def setUp(self):
        self._command = CreateBillingCommand(user_id=uuid.uuid4(),
                                             title='Gas Station',
                                             description='Yesterday',
                                             value=100.99,
                                             work_date=None)

        self._user_repository = Mock()
        self._user_repository.find_by_id.return_value = User()

        self._create_billing = CreateBilling(self._user_repository)

    def test_should_ensure_find_user_by_id(self):
        self._create_billing.execute(self._command)

        self._user_repository.find_by_id.assert_called_once()

    def test_should_ensure_save_user(self):
        self._create_billing.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_is_valid_true_when_billing_is_valid(self):
        self._create_billing.execute(self._command)

        self.assertTrue(self._create_billing.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.find_by_id.return_value = None

        self._create_billing.execute(self._command)

        self.assertFalse(self._create_billing.is_valid)

    def test_should_is_valid_false_when_billing_is_not_valid(self):
        command = CreateBillingCommand(user_id=uuid.uuid4(),
                                       title='Gas Station',
                                       description='Yesterday',
                                       value=-10,
                                       work_date=None)

        self._create_billing.execute(command)

        self.assertFalse(self._create_billing.is_valid)


class ConfirmReceiveBillingTests(unittest.TestCase):
    def setUp(self):
        self._steve = User()

        self._billing_summary = BillingSummary(title='Gas station security',
                                               description='Gas station security yesterday',
                                               value=100.50)

        self._billing = Billing(summary=self._billing_summary)

        self._user_repository = Mock()
        self._user_repository.find_by_id.return_value = self._steve
        self._user_repository.find_billing_by_id.return_value = self._billing

        self._command = ConfirmReceiveBillingCommand(user_id=self._steve.uid,
                                                     billing_id=self._billing.uid)

        self._confirm_receive_billing = ConfirmReceiveBilling(self._user_repository)

    def test_should_ensure_find_user_by_id(self):
        self._confirm_receive_billing.execute(self._command)

        self._user_repository.find_by_id.assert_called_once()

    def test_should_ensure_find_billing_by_id(self):
        self._confirm_receive_billing.execute(self._command)

        self._user_repository.find_billing_by_id.assert_called_once()

    def test_should_ensure_save_user(self):
        self._confirm_receive_billing.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.find_by_id.return_value = None

        self._confirm_receive_billing.execute(self._command)

        self.assertFalse(self._confirm_receive_billing.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        self._user_repository.find_billing_by_id.return_value = None

        self._confirm_receive_billing.execute(self._command)

        self.assertFalse(self._confirm_receive_billing.is_valid)

    def test_should_billing_is_received(self):
        self._steve.add_billing(self._billing)

        self._confirm_receive_billing.execute(self._command)

        self.assertTrue(self._billing.received)


class CancelReceiveBillingTests(unittest.TestCase):
    def setUp(self):
        self._steve = User()

        self._billing_summary = BillingSummary(title='Gas station security',
                                               description='Gas station security yesterday',
                                               value=100.50)

        self._billing = Billing(summary=self._billing_summary)

        self._command = CancelReceiveBillingCommand(user_id=self._steve.uid,
                                                    billing_id=self._billing.uid)

        self._user_repository = Mock()
        self._user_repository.find_by_id.return_value = self._steve
        self._user_repository.find_billing_by_id.return_value = self._billing

        self._cancel_receive_billing = CancelReceiveBilling(self._user_repository)

    def test_should_ensure_find_user_by_id(self):
        self._cancel_receive_billing.execute(self._command)

        self._user_repository.find_by_id.assert_called_once()

    def test_should_ensure_find_billing_by_id(self):
        self._cancel_receive_billing.execute(self._command)

        self._user_repository.find_billing_by_id.assert_called_once()

    def test_should_ensure_save_user(self):
        self._cancel_receive_billing.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.find_by_id.return_value = None

        self._cancel_receive_billing.execute(self._command)

        self.assertFalse(self._cancel_receive_billing.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        self._user_repository.find_billing_by_id.return_value = None

        self._cancel_receive_billing.execute(self._command)

        self.assertFalse(self._cancel_receive_billing.is_valid)

    def test_should_billing_is_not_received(self):
        self._steve.add_billing(self._billing)

        self._steve.confirm_receive(self._billing)

        self._cancel_receive_billing.execute(self._command)

        self.assertFalse(self._billing.received)


class UpdateBillingTests(unittest.TestCase):
    def setUp(self):
        self._steve = User()

        self._summary = BillingSummary(title='Gas station',
                                       description='Yesterday',
                                       value=100.99)

        self._billing = Billing(summary=self._summary)

        self._user_repository = Mock()
        self._user_repository.find_by_id.return_value = self._steve
        self._user_repository.find_billing_by_id.return_value = self._billing

        self._update_billing = UpdateBilling(self._user_repository)

        self._command = UpdateBillingCommand(user_id=self._steve.uid,
                                             billing_id=self._billing.uid,
                                             title='Gym',
                                             description='Tomorrow',
                                             value=200.99,
                                             work_date=datetime(day=9, month=2, year=2019))

    def test_should_ensure_find_user_by_id(self):
        self._update_billing.execute(self._command)

        self._user_repository.find_by_id.assert_called_once()

    def test_should_ensure_find_billing_by_id(self):
        self._update_billing.execute(self._command)

        self._user_repository.find_billing_by_id.assert_called_once()

    def test_should_ensure_save_user(self):
        self._update_billing.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.find_by_id.return_value = None

        self._update_billing.execute(self._command)

        self.assertFalse(self._update_billing.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        self._user_repository.find_billing_by_id.return_value = None

        self._update_billing.execute(self._command)

        self.assertFalse(self._update_billing.is_valid)

    def test_should_is_valid_false_when_summary_updated_not_is_valid(self):
        command = UpdateBillingCommand(user_id=self._steve.uid,
                                       billing_id=self._billing.uid,
                                       title='',
                                       description='',
                                       value=0,
                                       work_date=None)

        self._update_billing.execute(command)

        self.assertFalse(self._update_billing.is_valid)

    def test_should_update_billing_summary(self):
        self._steve.add_billing(self._billing)

        self._update_billing.execute(self._command)

        self.assertEqual(self._billing.title, self._command.title)
