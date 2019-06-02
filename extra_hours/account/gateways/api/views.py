from flask import Blueprint, request

from extra_hours.account.commands import (AuthenticateUserCommand,
                                          CreateUserCommand,
                                          ResetsPasswordCommand,
                                          ChangeUserPasswordCommand)
from extra_hours.shared.gateways.api.responses import bad_request, no_authorized, created, ok


def init_account_bp(app,
                    *,
                    get_create_user,
                    get_authenticate_user,
                    get_resets_password,
                    get_change_user_password):
    account_bp = Blueprint('account', __name__)

    @account_bp.route('/api/v1/account', methods=['post'])
    def create_user_view():
        json = request.get_json()

        command = CreateUserCommand(email=json['email'],
                                    password=json['password'])

        create_user = get_create_user()

        create_user.execute(command)

        if not create_user.is_valid:
            return bad_request([n.message for n in create_user.notifications])

        return created('user created')

    @account_bp.route('/api/v1/account/authenticate', methods=['post'])
    def authenticate_user_view():
        json = request.get_json()

        authenticate_user = get_authenticate_user()

        command = AuthenticateUserCommand(email=json['email'],
                                          password=json['password'])

        token = authenticate_user.execute(command)

        if not authenticate_user.is_valid:
            return no_authorized([n.message for n in authenticate_user.notifications])

        return ok(token)

    @account_bp.route('/api/v1/account/<string:email>/resets-password', methods=['post'])
    def resets_password_view(email):
        command = ResetsPasswordCommand(email=email)

        resets_password = get_resets_password()

        resets_password.execute(command)

        if not resets_password.is_valid:
            return bad_request([n.message for n in resets_password.notifications])

        return ok('password resets')

    @account_bp.route('/api/v1/account/<string:email>/change-password', methods=['post'])
    def change_user_password_view(email):
        json = request.get_json()

        command = ChangeUserPasswordCommand(email=email,
                                            old_password=json['old_password'],
                                            new_password=json['new_password'])

        change_user_password = get_change_user_password()

        change_user_password.execute(command)

        if not change_user_password.is_valid:
            return bad_request([n.message for n in change_user_password.notifications])

        return ok('password changed')

    app.register_blueprint(account_bp)

    return account_bp
