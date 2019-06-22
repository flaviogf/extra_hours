from sqlalchemy import exists

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
