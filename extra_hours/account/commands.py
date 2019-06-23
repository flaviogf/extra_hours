from dataclasses import dataclass


@dataclass
class CreateUserCommand:
    email: str
    password: str


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str


@dataclass
class ChangeUserPasswordCommand:
    email: str
    old_password: str
    new_password: str
