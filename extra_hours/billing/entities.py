from datetime import datetime
from functools import wraps

from extra_hours.shared.entities import Entity


def verify_billing_owner(func):
    @wraps(func)
    def wrapper(self, billing, *args, **kwargs):
        if billing not in self._billing:
            return

        return func(self, billing, *args, **kwargs)

    return wrapper


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

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'value': self.value,
            'work_date': self._format_work_date(),
            'received_date': self._format_received_date(),
            'received': self.received,
        }

    def _format_work_date(self):
        return self.work_date.strftime('%Y-%m-%d')

    def _format_received_date(self):
        return self.received_date.strftime('%Y-%m-%d') if self._received_date else None


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
