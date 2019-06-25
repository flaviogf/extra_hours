from extra_hours.billing.entities import User, Billing
from extra_hours.billing.queries import BillingListQueryResult
from extra_hours.shared.gateways.infra.uow import BillingTable, UserTable


class SqlAlchemyUserRepository:
    def __init__(self, uow):
        self._uow = uow

    def save_billing(self, user, billing):
        billing_table = self._uow.session.query(BillingTable).filter(BillingTable.uid == billing.uid).first()

        billing_table = billing_table or BillingTable()

        billing_table.uid = billing.uid
        billing_table.title = billing.title
        billing_table.description = billing.description
        billing_table.value = billing.value
        billing_table.work_date = billing.work_date
        billing_table.receive_date = billing.receive_date
        billing_table.received = billing.received
        billing_table.user_uid = user.uid

        self._uow.session.add(billing_table)

    def get_by_uid(self, uid):
        user_table = self._uow.session.query(UserTable).filter(UserTable.uid == uid).first()

        if not user_table:
            return

        return User(uid=user_table.uid)

    def get_billing_by_uid(self, user, uid):
        billing = (self._uow.session
                   .query(BillingTable)
                   .filter(BillingTable.uid == uid, BillingTable.user_uid == user.uid)
                   .first())

        if not billing:
            return

        return Billing(title=billing.title,
                       description=billing.description,
                       value=billing.value,
                       work_date=billing.work_date,
                       receive_date=billing.receive_date,
                       uid=billing.uid)

    def list_billing_received(self, user_uid, limit=10, offset=0):
        billing = (self._uow.session
                   .query(BillingTable)
                   .filter(BillingTable.user_uid == user_uid, BillingTable.received.is_(True))
                   .limit(limit)
                   .offset(offset))

        return [BillingListQueryResult(uid=it.uid,
                                       title=it.title,
                                       value=it.value) for it in billing]

    def list_billing_not_received(self, user_uid, limit=10, offset=0):
        billing = (self._uow.session
                   .query(BillingTable)
                   .filter(BillingTable.user_uid == user_uid, BillingTable.received.is_(False))
                   .limit(limit)
                   .offset(offset))

        return [BillingListQueryResult(uid=it.uid,
                                       title=it.title,
                                       value=it.value) for it in billing]

    def remove_billing(self, billing):
        billing_table = self._uow.session.query(BillingTable).filter(BillingTable.uid == billing.uid).first()

        self._uow.session.delete(billing_table)
