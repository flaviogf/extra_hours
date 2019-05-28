from os.path import dirname, join

from firebase_admin import credentials, initialize_app
from flask import Flask

from extra_hours.account.gateways.api.views import create_bp_account
from extra_hours.account.gateways.infra.repositories import FirebaseUserRepository
from extra_hours.account.gateways.infra.services import FirebaseUserService
from extra_hours.account.use_case import (AuthenticateUser,
                                          CreateUser,
                                          ResetsPassword,
                                          ChangeUserPassword)


def create_app():
    app = Flask(__name__)

    initialize_firebase()

    bp_account = create_bp_account(get_create_user,
                                   get_authenticate_user,
                                   get_resets_password,
                                   get_change_user_password)

    app.register_blueprint(bp_account)

    return app


def get_create_user():
    user_repository = FirebaseUserRepository()
    return CreateUser(user_repository)


def get_authenticate_user():
    user_service = FirebaseUserService()
    return AuthenticateUser(user_service)


def get_resets_password():
    user_repository = FirebaseUserRepository()
    return ResetsPassword(user_repository)


def get_change_user_password():
    user_repository = FirebaseUserRepository()
    user_service = FirebaseUserService()
    return ChangeUserPassword(user_repository, user_service)


def initialize_firebase():
    root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))
    certificate_path = join(root_path, '.firebase.json')
    cred = credentials.Certificate(certificate_path)
    initialize_app(cred)
