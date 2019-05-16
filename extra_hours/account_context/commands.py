from dataclasses import dataclass


@dataclass
class CreateUserCommand:
    email: str
    password: str
