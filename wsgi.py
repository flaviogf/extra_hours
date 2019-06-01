from os.path import dirname, join

from firebase_admin import credentials, initialize_app
from flask import Flask

from extra_hours.account.gateways.api.views import create_account_bp
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository as AccountFirebaseUserRepository
from extra_hours.account.gateways.infra.services import FirebaseUserService
from extra_hours.account.use_case import (AuthenticateUser,
                                          CreateUser,
                                          ResetsPassword,
                                          ChangeUserPassword)
from extra_hours.billing.gateways.api.views import create_billing_bp
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository as BillingFirebaseUserRepository
from extra_hours.billing.use_case import (CreateBilling,
                                          ConfirmReceiveBilling,
                                          CancelReceiveBilling,
                                          UpdateBilling)


class Config:
    SECRET_KEY = ')u=#7@=e7$w1ea06wz%)c=w(h9vdn!^4($@tl7^fd=m5u6mvb^'


def get_create_user():
    user_repository = AccountFirebaseUserRepository()
    return CreateUser(user_repository)


def get_authenticate_user():
    user_service = FirebaseUserService(Config)
    return AuthenticateUser(user_service)


def get_resets_password():
    user_repository = AccountFirebaseUserRepository()
    return ResetsPassword(user_repository)


def get_change_user_password():
    user_repository = AccountFirebaseUserRepository()
    user_service = FirebaseUserService(Config)
    return ChangeUserPassword(user_repository, user_service)


def get_create_billing():
    user_repository = BillingFirebaseUserRepository()
    return CreateBilling(user_repository)


def get_confirm_receive_billing():
    user_repository = BillingFirebaseUserRepository()
    return ConfirmReceiveBilling(user_repository)


def get_cancel_receive_billing():
    user_repository = BillingFirebaseUserRepository()
    return CancelReceiveBilling(user_repository)


def get_update_billing():
    user_repository = BillingFirebaseUserRepository()
    return UpdateBilling(user_repository)


def initialize_firebase():
    root_path = dirname(__file__)
    certificate_path = join(root_path, '.firebase.json')
    cred = credentials.Certificate(certificate_path)
    initialize_app(cred)


app = Flask(__name__)

initialize_firebase()

bp_account = create_account_bp(get_create_user,
                               get_authenticate_user,
                               get_resets_password,
                               get_change_user_password)

billing_bp = create_billing_bp(get_create_billing,
                               get_confirm_receive_billing,
                               get_cancel_receive_billing,
                               get_update_billing)

app.register_blueprint(bp_account)
app.register_blueprint(billing_bp)

if __name__ == '__main__':
    app.run()
