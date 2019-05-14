from pyflunt.notifications import Notifiable

from extra_hours.billing_context.entities import User, Billing


class UseCase(Notifiable):
    pass


class CreateBilling(UseCase):
    def __init__(self, user_repository):
        super().__init__()
        self._user_repository = user_repository

    def execute(self, command):
        user = User(uid=command.user_id)

        billing = Billing(title=command.title,
                          description=command.description,
                          value=command.value,
                          work_date=command.work_date)

        if not user.is_valid or not billing.is_valid:
            self.add_notifications(user, billing)

            return

        user.add_billing(billing)

        self._user_repository.save(user)
