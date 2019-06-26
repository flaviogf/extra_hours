from pyflunt.notifications import Notification

from extra_hours.billing.entities import Billing
from extra_hours.shared.use_cases import UseCase


class AddBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.get_by_uid(command.user_uid)

        if not user:
            self.add_notifications(Notification('user', 'user not exists'))
            return

        billing = Billing(title=command.title,
                          description=command.description,
                          value=command.value,
                          work_date=command.work_date)

        user.add_billing(billing)

        self.add_notifications(user, billing)

        if not self.is_valid:
            return

        for billing in user.billing:
            self._user_repository.save_billing(user, billing)


class ConfirmReceiveBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.get_by_uid(command.user_uid)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        billing = self._user_repository.get_billing_by_uid(user, command.billing_uid)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))

        if not self.is_valid:
            return

        user.confirm_receive_billing(billing)

        self._user_repository.save_billing(user, billing)


class CancelReceiveBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.get_by_uid(command.user_uid)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        billing = self._user_repository.get_billing_by_uid(user, command.billing_uid)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))

        if not self.is_valid:
            return

        user.cancel_receive_billing(billing)

        self._user_repository.save_billing(user, billing)


class RemoveBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.get_by_uid(command.user_uid)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        billing = self._user_repository.get_billing_by_uid(user, command.billing_uid)

        if not billing:
            self.add_notification(Notification('billing', 'billing not exists'))
            return

        self._user_repository.remove_billing(billing)


class UpdateBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()

        self._user_repository = user_repository

    def execute(self, command):
        user = self._user_repository.get_by_uid(command.user_uid)

        if not user:
            self.add_notification(Notification('user', 'user not exists'))
            return

        billing = self._user_repository.get_billing_by_uid(user, command.billing_uid)

        if not billing:
            self.add_notification(Notification('Billing', 'billing not exists'))
            return

        billing = Billing(title=command.title,
                          description=command.description,
                          value=command.value,
                          work_date=command.work_date,
                          receive_date=billing.receive_date,
                          uid=billing.uid)

        self._user_repository.save_billing(user, billing)
