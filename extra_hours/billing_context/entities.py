from datetime import datetime

from pyflunt.notifications import Notifiable
from pyflunt.validations import Contract


class Billing(Notifiable):
    def __init__(self, title, description, value, work_date=None):
        super().__init__()
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
