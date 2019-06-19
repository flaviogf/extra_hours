from extra_hours.billing.entities import User, Billing
from extra_hours.billing.value_objects import BillingSummary
from extra_hours.shared.gateways.infra.uow import UserTable, BillingTable


class SqlAlchemyUserRepository:
    def __init__(self, session):
        self._session = session

    def add(self, user):
        for it in user.billing:
            billing = self._session.query(BillingTable).filter(BillingTable.uid == it.uid).first()

            billing = billing or BillingTable()

            billing.uid = it.uid
            billing.title = it.title
            billing.description = it.description
            billing.value = it.value
            billing.work_date = it.work_date
            billing.received_date = it.received_date
            billing.user_uid = user.uid

            self._session.add(billing)

    def get_by_id(self, uid):
        user = self._session.query(UserTable).filter(UserTable.uid == uid).first()

        if not user:
            return

        return User(uid=user.uid)

    def get_billing_by_id(self, billing_uid):
        billing_table = self._session.query(BillingTable).filter(BillingTable.uid == billing_uid).first()

        if not billing_table:
            return

        summary = BillingSummary(title=billing_table.title,
                                 description=billing_table.description,
                                 value=billing_table.value,
                                 work_date=billing_table.work_date)

        billing = Billing(summary=summary, uid=billing_table.uid)

        return billing
