import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.repositories import SqlAlchemyUserRepository
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.gateways.infra.uow import UserTable, Base


class SqlAlchemyUserRepositoryTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self._session = Session()

        self._user_repository = SqlAlchemyUserRepository(self._session)

    def test_should_add_create_user_when_not_exits(self):
        naruto = User(email=Email('naruto@uzumaki.com'), password=Password('test123'))

        self._user_repository.add(naruto)

        users = self._session.query(UserTable).all()

        self.assertEqual(1, len(users))

    def test_should_add_update_user_when_exits(self):
        naruto = User(email=Email('naruto@uzumaki.com'), password=Password('test123'))

        self._user_repository.add(naruto)

        updated = User(email=Email('naruto@uzumaki.com'), password=Password('test123'), uid=naruto.uid)

        self._user_repository.add(updated)

        users = self._session.query(UserTable).all()

        self.assertEqual(1, len(users))

    def test_should_get_by_email_return_user_when_exists(self):
        naruto = User(email=Email('naruto@uzumaki.com'), password=Password('test123'))

        self._user_repository.add(naruto)

        user = self._user_repository.get_by_email('naruto@uzumaki.com')

        self.assertIsInstance(user, User)

    def test_should_get_by_email_return_none_when_not_exists(self):
        user = self._user_repository.get_by_email('naruto@uzumaki.com')

        self.assertIsNone(user)

    def test_should_check_email_return_true_when_available(self):
        available = self._user_repository.check_email('naruto@uzumaki.com')

        self.assertTrue(available)

    def test_should_check_email_return_false_when_not_available(self):
        naruto = User(email=Email('naruto@uzumaki.com'), password=Password('test123'))

        self._user_repository.add(naruto)

        available = self._user_repository.check_email('naruto@uzumaki.com')

        self.assertFalse(available)
