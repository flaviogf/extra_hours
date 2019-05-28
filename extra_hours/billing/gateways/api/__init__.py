from os.path import dirname, join

from firebase_admin import credentials, initialize_app
from flask import Flask

from extra_hours.billing.gateways.api.views import create_billing_bp
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.billing.use_case import CreateBilling, ConfirmReceiveBilling, CancelReceiveBilling, UpdateBilling


def create_app():
    app = Flask(__name__)

    initialize_firebase()

    billing_bp = create_billing_bp(get_create_billing,
                                   get_confirm_receive_billing,
                                   get_cancel_receive_billing,
                                   get_update_billing)

    app.register_blueprint(billing_bp)

    return app


def get_create_billing():
    user_repository = FirebaseUserRepository()
    return CreateBilling(user_repository)


def get_confirm_receive_billing():
    user_repository = FirebaseUserRepository()
    return ConfirmReceiveBilling(user_repository)


def get_cancel_receive_billing():
    user_repository = FirebaseUserRepository()
    return CancelReceiveBilling(user_repository)


def get_update_billing():
    user_repository = FirebaseUserRepository()
    return UpdateBilling(user_repository)


def initialize_firebase():
    root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))
    certificate_path = join(root_path, '.firebase.json')
    cred = credentials.Certificate(certificate_path)
    initialize_app(cred)
