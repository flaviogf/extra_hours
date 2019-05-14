from extra_hours.billing_context.commands import CommandResult
from extra_hours.billing_context.entities import User, Billing


class CreateBilling:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def execute(self, command):
        user = User(uid=command.user_id)

        billing = Billing(title=command.title,
                          description=command.description,
                          value=command.value,
                          work_date=command.work_date)

        if not user.is_valid or not billing.is_valid:
            return CommandResult(success=False,
                                 message='Billing not created',
                                 data=user.notifications + billing.notifications)

        user.add_billing(billing)

        self._user_repository.save(user)

        return CommandResult(success=True,
                             message='Billing created with success',
                             data=billing)
