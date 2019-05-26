from flask import Flask

from extra_hours.billing.gateways.api.views import create_billing_bp
from extra_hours.billing.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.billing.use_case import CreateBilling


def get_create_billing():
    user_repository = FirebaseUserRepository()
    return CreateBilling(user_repository)


def create_app():
    app = Flask(__name__)

    billing_bp = create_billing_bp(get_create_billing)

    app.register_blueprint(billing_bp)

    return app
