import unittest
import uuid
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.repositories import SqlAlchemyUserRepository
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.gateways.infra.uow import Base, UserTable


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')

        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

        uow = Mock()
        uow.session = self._session

        self._user_repository = SqlAlchemyUserRepository(uow)

    def test_should_save_create_user_when_user_not_exists(self):
        naruto = User(Email('naruto@uzuamki.com'), Password('test123'))

        self._user_repository.save(naruto)

        expected = 1

        result = self._session.query(UserTable).count()

        self.assertEqual(expected, result)

    def test_should_save_update_user_when_user_exists(self):
        naruto_table = UserTable(uid=str(uuid.uuid4()), email='naruto@uzuamki.com', password='test123')

        self._session.add(naruto_table)

        naruto = User(Email('naruto@uzuamki.com'), Password('test123'), uid=naruto_table.uid)

        self._user_repository.save(naruto)

        expected = 1

        result = self._session.query(UserTable).count()

        self.assertEqual(expected, result)

    def test_should_check_email_return_true_when_email_is_available(self):
        naruto = UserTable(uid=str(uuid.uuid4()), email='naruto@uzuamki.com', password='test123')

        self._session.add(naruto)

        email_available = self._user_repository.check_email('sasuke@uchiha.com')

        self.assertTrue(email_available)

    def test_should_check_email_return_false_when_email_not_is_available(self):
        naruto = UserTable(uid=str(uuid.uuid4()), email='naruto@uzuamki.com', password='test123')

        self._session.add(naruto)

        email_available = self._user_repository.check_email('naruto@uzuamki.com')

        self.assertFalse(email_available)
