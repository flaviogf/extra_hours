import unittest
import uuid
from unittest.mock import Mock

from extra_hours.billing_context.commands import CreateBillingCommand
from extra_hours.billing_context.use_case import CreateBilling


class CreateBillingTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = Mock()

        self._create_billing = CreateBilling(self._user_repository)

        self._command = CreateBillingCommand(user_id=uuid.uuid4(),
                                             title='Gas Station',
                                             description='Yesterday',
                                             value=100.99,
                                             work_date=None)

    def test_should_execute_not_raise_error(self):
        self._create_billing.execute(self._command)

    def test_should_execute_save_user(self):
        self._create_billing.execute(self._command)

        self._user_repository.save.assert_called_once()

    def test_should_execute_return_command_with_success_equal_to_true_when_command_is_valid(self):
        result = self._create_billing.execute(self._command)

        self.assertTrue(result.success)

    def test_should_execute_return_command_with_success_equal_to_false_when_command_is_invalid(self):
        command = CreateBillingCommand(user_id=uuid.uuid4(),
                                       title='Gas Station',
                                       description='Yesterday',
                                       value=-10,
                                       work_date=None)

        result = self._create_billing.execute(command)

        self.assertFalse(result.success)
