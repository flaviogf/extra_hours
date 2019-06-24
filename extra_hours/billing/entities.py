from decimal import Decimal

from datetime import datetime
from pyflunt.validations import Contract

from extra_hours.shared.entities import Entity


class User(Entity):
    def __init__(self, uid=None):
        super().__init__(uid=uid)

        self._billing = []

    @property
    def billing(self):
        return tuple(self._billing)

    def add_billing(self, billing):
        self._billing.append(billing)

    def confirm_receive_billing(self, billing):
        billing.confirm_receive()


class Billing(Entity):
    def __init__(self, title, description, value, work_date, receive_date=None, uid=None):
        super().__init__(uid=uid)

        self._title = title
        self._description = description
        self._value = value
        self._work_date = work_date
        self._receive_date = receive_date

        self.add_notifications(Contract()
                               .requires()
                               .is_not_none_or_empty(value=title,
                                                     field='title',
                                                     message='title should be informed')
                               .is_not_none_or_empty(value=description,
                                                     field='description',
                                                     message='description should be informed')
                               .is_greater_than(value=value,
                                                comparer=Decimal(0),
                                                field='value',
                                                message='value should be greater than zero')
                               .is_true(value=self._receive_date_is_valid(),
                                        field='receive_date',
                                        message='receive date should be greater than work date'))

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
    def receive_date(self):
        return self._receive_date

    @property
    def received(self):
        return bool(self._receive_date)

    def confirm_receive(self):
        self._receive_date = datetime.now()

    def _receive_date_is_valid(self):
        return True if not self._receive_date or self._receive_date > self._work_date else False
