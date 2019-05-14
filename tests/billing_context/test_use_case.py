import unittest
import uuid
from unittest.mock import Mock

from extra_hours.billing_context.commands import CreateBillingCommand, ConfirmReceiveBillingCommand
from extra_hours.billing_context.entities import User, Billing
from extra_hours.billing_context.use_case import CreateBilling, ConfirmReceiveBilling


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

        self._billing = Billing(title='Gas station',
                                description='Yesterday',
                                value=100)

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
