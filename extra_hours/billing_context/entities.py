import uuid
from datetime import datetime

from pyflunt.notifications import Notifiable
from pyflunt.validations import Contract


class Entity(Notifiable):
    def __init__(self, uid=None):
        super().__init__()
        self.uid = uid or uuid.uuid4()

    def __eq__(self, other):
        return self.uid == other.uid


class Billing(Entity):
    def __init__(self, title, description, value, work_date=None, uid=None):
        super().__init__(uid=uid)
        self._title = title
        self._description = description
        self._value = value
        self._work_date = work_date or datetime.now()
        self._received_date = None

        self.add_notifications(Contract()
                               .requires()
                               .has_min_len(title, 3, 'title', 'invalid title')
                               .has_min_len(description, 3, 'description', 'invalid description')
                               .is_greater_than(value, 0, 'value', 'invalid value'))

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def value(self):
        return self._value

    @property
    def work_date(self):
        return self._work_date

    @property
    def received_date(self):
        return self._received_date

    @property
    def received(self):
        return self._received_date is not None

    def confirm_receive(self):
        self._received_date = datetime.now()

    def cancel_receive(self):
        self._received_date = None


class User(Entity):
    def __init__(self, uid=None):
        super().__init__(uid=uid)
        self._billing = []

    @property
    def billing(self):
        return tuple(self._billing)

    @property
    def billing_received(self):
        return tuple((it for it in self._billing if it.received))

    @property
    def billing_not_received(self):
        return tuple((it for it in self._billing if not it.received))

    def add_billing(self, billing):
        self._billing.append(billing)

    def confirm_receive(self, billing):
        if billing not in self._billing:
            return

        billing.confirm_receive()

    def cancel_receive(self, billing):
        if billing not in self._billing:
            return

        billing.cancel_receive()
