import unittest
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock

from extra_hours.billing.commands import AddBillingCommand, ConfirmReceiveBillingCommand, CancelReceiveBillingCommand, \
    RemoveBillingCommand
from extra_hours.billing.entities import User, Billing
from extra_hours.billing.use_cases import AddBilling, ConfirmReceiveBilling, CancelReceiveBilling, RemoveBilling


class AddBillingTests(unittest.TestCase):
    def test_should_is_valid_true_when_billing_added(self):
        user_repository = Mock()

        user_repository.get_by_uid.return_value = User(uid=str(uuid.uuid4()))

        yesterday = datetime.now() + timedelta(days=1)

        command = AddBillingCommand(user_uid=str(uuid.uuid4()),
                                    title='Gas Station',
                                    description='Yesterday',
                                    value=Decimal(10),
                                    work_date=yesterday)

        use_case = AddBilling(user_repository)

        use_case.execute(command)

        self.assertTrue(use_case.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        user_repository = Mock()

        user_repository.get_by_uid.return_value = None

        yesterday = datetime.now() + timedelta(days=1)

        command = AddBillingCommand(user_uid=str(uuid.uuid4()),
                                    title='Gas Station',
                                    description='Yesterday',
                                    value=Decimal(10),
                                    work_date=yesterday)

        use_case = AddBilling(user_repository)

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)

    def test_should_is_valid_false_when_billing_added_not_is_valid(self):
        user_repository = Mock()

        user_repository.get_by_uid.return_value = User(uid=str(uuid.uuid4()))

        yesterday = datetime.now() + timedelta(days=1)

        command = AddBillingCommand(user_uid=str(uuid.uuid4()),
                                    title='',
                                    description='Yesterday',
                                    value=Decimal(10),
                                    work_date=yesterday)

        use_case = AddBilling(user_repository)

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)


class ConfirmReceiveBillingTests(unittest.TestCase):
    def test_should_is_valid_true_when_confirm_receive_billing(self):
        user_repository = Mock()
        user_repository.get_by_uid.return_value = User()
        user_repository.get_billing_by_uid.return_value = Billing(title='Gas Station',
                                                                  description='Yesterday',
                                                                  value=Decimal(100),
                                                                  work_date=datetime.now())

        command = ConfirmReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                               billing_uid=str(uuid.uuid4()))

        use_case = ConfirmReceiveBilling(user_repository)

        use_case.execute(command)

        self.assertTrue(use_case.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        user_repository = Mock()
        user_repository.get_by_uid.return_value = User()
        user_repository.get_billing_by_uid.return_value = None

        command = ConfirmReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                               billing_uid=str(uuid.uuid4()))

        use_case = ConfirmReceiveBilling(user_repository)

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        user_repository = Mock()
        user_repository.get_by_uid.return_value = None
        user_repository.get_billing_by_uid.return_value = Billing(title='Gas Station',
                                                                  description='Yesterday',
                                                                  value=Decimal(100),
                                                                  work_date=datetime.now())

        command = ConfirmReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                               billing_uid=str(uuid.uuid4()))

        use_case = ConfirmReceiveBilling(user_repository)

        use_case.execute(command)

        self.assertFalse(use_case.is_valid)


class CancelReceiveBillingTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = Mock()

        self._use_case = CancelReceiveBilling(self._user_repository)

    def test_should_is_valid_true_when_cancel_receive_billing(self):
        self._user_repository.get_by_uid.return_value = User()
        self._user_repository.get_billing_by_uid.return_value = Billing(title='Gas Station',
                                                                        description='Yesterday',
                                                                        value=Decimal(10),
                                                                        work_date=datetime.now())

        command = CancelReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                              billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertTrue(self._use_case.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.get_by_uid.return_value = None

        command = CancelReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                              billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        self._user_repository.get_by_uid.return_value = User()
        self._user_repository.get_billing_by_uid.return_value = None

        command = CancelReceiveBillingCommand(user_uid=str(uuid.uuid4()),
                                              billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)


class RemoveBillingTests(unittest.TestCase):
    def setUp(self):
        self._user_repository = Mock()

        self._use_case = RemoveBilling(self._user_repository)

    def test_should_is_valid_true_when_remove_billing(self):
        self._user_repository.get_billing_by_uid.return_value = Billing(title='',
                                                                        description='',
                                                                        value=Decimal(10),
                                                                        work_date=datetime.now(),
                                                                        uid=str(uuid.uuid4()))
        self._user_repository.get_by_uid.return_value = User()

        command = RemoveBillingCommand(user_uid=str(uuid.uuid4()),
                                       billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertTrue(self._use_case.is_valid)

    def test_should_is_valid_false_when_user_not_exists(self):
        self._user_repository.get_billing_by_uid.return_value = Billing(title='',
                                                                        description='',
                                                                        value=Decimal(10),
                                                                        work_date=datetime.now(),
                                                                        uid=str(uuid.uuid4()))
        self._user_repository.get_by_uid.return_value = None

        command = RemoveBillingCommand(user_uid=str(uuid.uuid4()),
                                       billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)

    def test_should_is_valid_false_when_billing_not_exists(self):
        self._user_repository.get_billing_by_uid.return_value = None
        self._user_repository.get_by_uid.return_value = User()

        command = RemoveBillingCommand(user_uid=str(uuid.uuid4()),
                                       billing_uid=str(uuid.uuid4()))

        self._use_case.execute(command)

        self.assertFalse(self._use_case.is_valid)
