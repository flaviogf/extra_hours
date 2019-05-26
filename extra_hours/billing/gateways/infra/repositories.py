from extra_hours.billing.entities import User


class FirebaseUserRepository:
    def find_by_id(self, uid):
        return User(uid=uid)

    def save(self, user):
        pass
