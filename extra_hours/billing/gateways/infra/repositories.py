import uuid
from datetime import datetime

from firebase_admin import firestore
from firebase_admin.auth import AuthError, get_user

from extra_hours.billing.entities import User, Billing
from extra_hours.billing.value_objects import BillingSummary


class FirebaseUserRepository:
    def find_by_id(self, uid):
        try:
            user_record = get_user(str(uid))
        except (AuthError, ValueError):
            return None
        else:
            uid = uuid.UUID(user_record.uid)
            user = User(uid=uid)
            return user

    def save(self, user):
        db = firestore.client()

        user_collection = db.collection('user')

        user_document = user_collection.document(str(user.uid))

        billing_collection = user_document.collection('billing')

        for billing in user.billing:
            billing_document = billing_collection.document(str(billing.uid))
            billing_document.set(billing.to_dict())

    def find_billing_by_id(self, billing_id):
        db = firestore.client()

        users = db.collection('user').list_documents()

        billings = [b.get().to_dict() for u in users
                    for b in u.collection('billing').list_documents()
                    if b.id == str(billing_id)]

        billing_dict = billings[0] if billings else None

        if not billing_dict:
            return

        work_date = billing_dict['work_date']

        work_date = datetime.strptime(work_date, '%Y-%m-%d')

        summary = BillingSummary(title=billing_dict['title'],
                                 description=billing_dict['description'],
                                 value=billing_dict['value'],
                                 work_date=work_date)

        return Billing(summary=summary, uid=billing_id)
