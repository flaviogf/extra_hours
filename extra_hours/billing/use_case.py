from pyflunt.notifications import Notification

from extra_hours.billing.entities import Billing
from extra_hours.billing.value_objects import BillingSummary
from extra_hours.shared.use_case import UseCase


class CreateBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.find_by_id(command.user_id)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))

        summary = BillingSummary(title=command.title,
                                 description=command.description,
                                 value=command.value,
                                 work_date=command.work_date)

        billing = Billing(summary=summary)

        self.add_notifications(billing)

        if not self.is_valid:
            return

        user.add_billing(billing)

        self._user_repository.save(user)


class ConfirmReceiveBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.find_by_id(command.user_id)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))

        billing = self._user_repository.find_billing_by_id(command.billing_id)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))

        if not self.is_valid:
            return

        user.add_billing(billing)

        user.confirm_receive(billing)

        self._user_repository.save(user)


class CancelReceiveBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.find_by_id(command.user_id)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))

        billing = self._user_repository.find_billing_by_id(command.billing_id)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))

        if not self.is_valid:
            return

        user.cancel_receive(billing)

        self._user_repository.save(user)


class UpdateBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.find_by_id(command.user_id)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))

        billing = self._user_repository.find_billing_by_id(command.billing_id)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))

        billing_summary = BillingSummary(title=command.title,
                                         description=command.description,
                                         value=command.value,
                                         work_date=command.work_date)

        self.add_notifications(billing_summary)

        if not self.is_valid:
            return

        user.update_billing_summary(billing, billing_summary)

        self._user_repository.save(user)
