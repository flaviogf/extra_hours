from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.gateways.infra.uow import UserTable


class SqlAlchemyUserRepository:
    def __init__(self, session):
        self._session = session

    def add(self, user):
        user_table = self._session.query(UserTable).filter(UserTable.uid == user.uid).first()
        user_table = user_table if user_table else UserTable()
        user_table.uid = user.uid
        user_table.email = user.email
        user_table.password = user.password
        self._session.add(user_table)

    def get_by_email(self, email):
        user_table = self._session.query(UserTable).filter(UserTable.email == email).first()

        if not user_table:
            return

        return User(email=Email(user_table.email),
                    password=Password(user_table.password, encrypt=False),
                    uid=user_table.uid)

    def check_email(self, email):
        user = self._session.query(UserTable).filter(UserTable.email == email).first()
        return not user
