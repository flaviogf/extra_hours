import uuid

from firebase_admin import firestore
from firebase_admin.auth import AuthError, get_user

from extra_hours.billing.entities import User


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
