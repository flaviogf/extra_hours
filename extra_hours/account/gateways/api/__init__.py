from flask import Flask

from extra_hours.account.gateways.api.views import create_account
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.account.use_case import CreateUser


def create_app():
    app = Flask(__name__)

    def get_create_user():
        user_repository = FirebaseUserRepository()
        return CreateUser(user_repository)

    account = create_account(get_create_user)

    app.register_blueprint(account)

    return app
