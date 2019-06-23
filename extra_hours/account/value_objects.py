import hashlib

from pyflunt.validations import Contract

from extra_hours.shared.value_objects import ValueObject


class Email(ValueObject):
    def __init__(self, value):
        super().__init__()

        self._value = value

        self.add_notifications(Contract()
                               .requires()
                               .is_email(value=value,
                                         field='email',
                                         message='email not is valid'))

    def __str__(self):
        return self._value


class Password(ValueObject):
    def __init__(self, value, encrypt=True):
        super().__init__()

        self._value = self._encrypt(value) if encrypt else value

        self.add_notifications(Contract()
                               .requires()
                               .has_min_len(value=value,
                                            minimum=6,
                                            field='password',
                                            message='password should be min len 6')
                               .match(value=value,
                                      pattern=r'(?=.*[a-zA-Z]+).*',
                                      field='password',
                                      message='password should be alphabetic character')
                               .match(value=value,
                                      pattern=r'(?=.*\d+).*',
                                      field='password',
                                      message='password should be numeric character'))

    @staticmethod
    def _encrypt(value):
        return hashlib.md5(value.encode()).hexdigest()

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return str(self) == str(other)
