from collections import namedtuple

CreateUserCommand = namedtuple('CreateUserCommand', ['email', 'password'])

AuthenticateUserCommand = namedtuple('AuthenticateUserCommand', ['email', 'password'])

ResetsPasswordCommand = namedtuple('ResetsPasswordCommand', ['email'])

ChangeUserPasswordCommand = namedtuple('ChangeUserPasswordCommand', ['email', 'old_password', 'new_password'])
