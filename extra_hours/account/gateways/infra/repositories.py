from sqlalchemy import exists

from extra_hours.account.entities import User
from extra_hours.account.value_objects import Email, Password
from extra_hours.shared.gateways.infra.uow import UserTable


class SqlAlchemyUserRepository:
    def __init__(self, uow):
        self._uow = uow

    def save(self, user):
        user_table = self._uow.session.query(UserTable).filter(UserTable.uid == user.uid).first()

        user_table = user_table or UserTable(uid=user.uid,
                                             email=user.email,
                                             password=user.password)

        self._uow.session.add(user_table)

    def check_email(self, email):
        return not (self._uow.session
                    .query(exists().where(UserTable.email == email))
                    .scalar())

    def get_by_email(self, email):
        user_table = self._uow.session.query(UserTable).filter(UserTable.email == email).first()

        if not user_table:
            return

        user = User(email=Email(user_table.email),
                    password=Password(user_table.password, encrypt=False),
                    uid=user_table.uid)

        return user
