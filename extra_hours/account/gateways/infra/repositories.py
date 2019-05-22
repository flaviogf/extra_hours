from os.path import dirname, join

import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import create_user, get_user_by_email, AuthError

root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))

certificate_path = join(root_path, '.firebase.json')

cred = credentials.Certificate(certificate_path)

firebase_admin.initialize_app(cred)


class FirebaseUserRepository:
    def check_email(self, email):
        try:
            get_user_by_email(email)
            return False
        except (AuthError, ValueError):
            return True

    def save(self, user):
        create_user(**user.to_dict())
