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
class ResetsPasswordCommand:
    email: str
