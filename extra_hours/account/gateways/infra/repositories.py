from firebase_admin.auth import create_user, get_user_by_email, AuthError


class FirebaseUserRepository:
    def check_email(self, email):
        try:
            get_user_by_email(email)
            return False
        except (AuthError, ValueError):
            return True

    def save(self, user):
        create_user(**user.to_dict())
