from pyflunt.validations import Contract

from extra_hours.shared.value_objects import ValueObject


class Password(ValueObject):
    def __init__(self, password):
        super().__init__()
        self._password = password

        self.add_notifications(Contract()
                               .requires()
                               .has_min_len(value=password,
                                            minimum=6,
                                            field='password',
                                            message='password should be min len 6')
                               .match(value=password,
                                      pattern=r'(?=.*[a-zA-Z]+).*',
                                      field='password',
                                      message='password should be alphabetic character')
                               .match(value=password,
                                      pattern=r'(?=.*\d+).*',
                                      field='password',
                                      message='password should be numeric character'))

    def __str__(self):
        return self._password


class Email(ValueObject):
    def __init__(self, email):
        super().__init__()
        self._email = email

        self.add_notifications(Contract()
                               .requires()
                               .is_email(value=email,
                                         field='email',
                                         message='invalid email'))

    def __str__(self):
        return self._email
