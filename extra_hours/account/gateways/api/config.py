from unittest.mock import Mock

from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.account.use_case import CreateUser


class Config:
    USER_REPOSITORY = FirebaseUserRepository()
    CREATE_USER = CreateUser(USER_REPOSITORY)


class TestingConfig(Config):
    USER_REPOSITORY = Mock()
    CREATE_USER = Mock()
