import unittest
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock

from extra_hours.billing.commands import AddBillingCommand
from extra_hours.billing.entities import User
from extra_hours.billing.use_cases import AddBilling


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
