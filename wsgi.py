from datetime import datetime
from os.path import dirname, join

from firebase_admin import credentials, initialize_app
from flask import Flask
from flask_caching import Cache

from extra_hours.account.gateways.api.middlewares import init_account_middleware
from extra_hours.account.gateways.api.views import init_account_bp
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository as AccountFirebaseUserRepository
from extra_hours.account.gateways.infra.services import FirebaseUserService
from extra_hours.account.use_case import (AuthenticateUser,
                                          CreateUser,
                                          ResetsPassword,
                                          ChangeUserPassword)
from extra_hours.billing.gateways.api.views import init_billing_bp
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository as BillingFirebaseUserRepository
from extra_hours.billing.use_case import (CreateBilling,
                                          ConfirmReceiveBilling,
                                          CancelReceiveBilling,
                                          UpdateBilling)
from extra_hours.shared.gateways.api.responses import ok


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

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

initialize_firebase()

init_account_middleware(app, Config)

init_account_bp(app,
                get_create_user=get_create_user,
                get_authenticate_user=get_authenticate_user,
                get_resets_password=get_resets_password,
                get_change_user_password=get_change_user_password)

init_billing_bp(app,
                get_create_billing=get_create_billing,
                get_confirm_receive_billing=get_confirm_receive_billing,
                get_cancel_receive_billing=get_cancel_receive_billing,
                get_update_billing=get_update_billing)


@app.route('/')
@cache.cached(300)
def index():
    return ok(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    app.run()
