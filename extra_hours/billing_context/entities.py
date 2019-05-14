import uuid
from datetime import datetime

from pyflunt.notifications import Notifiable

from functools import wraps


def verify_billing_owner(func):
    @wraps(func)
    def wrapper(self, billing, *args, **kwargs):
        if billing not in self._billing:
            return

        return func(self, billing, *args, **kwargs)

    return wrapper


class Entity(Notifiable):
    def __init__(self, uid=None):
        super().__init__()
        self.uid = uid or uuid.uuid4()

    def __eq__(self, other):
        return self.uid == other.uid


class Billing(Entity):
    def __init__(self, summary, uid=None):
        super().__init__(uid=uid)
        self._summary = summary
        self._received_date = None

        self.add_notifications(summary)

    @property
    def title(self):
        return self._summary.title

    @property
    def description(self):
        return self._summary.description

    @property
    def value(self):
        return self._summary.value

    @property
    def work_date(self):
        return self._summary.work_date

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

    def update_summary(self, summary):
        self._summary = summary

        self.add_notifications(summary)


class User(Entity):
    def __init__(self, billing=(), uid=None):
        super().__init__(uid=uid)
        self._billing = list(billing)

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

    @verify_billing_owner
    def confirm_receive(self, billing):
        billing.confirm_receive()

    @verify_billing_owner
    def cancel_receive(self, billing):
        billing.cancel_receive()

    @verify_billing_owner
    def update_billing_summary(self, billing, summary):
        billing.update_summary(summary)
