from firebase_admin.auth import (AuthError, create_user, get_user_by_email,
                                 update_user)

from extra_hours.account.entities import User


class FirebaseUserRepository:
    def check_email(self, email):
        try:
            get_user_by_email(email)
            return False
        except (AuthError, ValueError):
            return True

    def save(self, user):
        user_dict = user.to_dict()

        try:
            get_user_by_email(user_dict['email'])
        except (AuthError):
            create_user(**user_dict)
        else:
            update_user(**user_dict)

    def find_by_email(self, email):
        try:
            user = get_user_by_email(email)
        except (AuthError, ValueError):
            return None
        else:
            user = User(email=user.email, password='', uid=user.uid)

            return user
