from flask import Blueprint, request, jsonify

from extra_hours.account.commands import CreateUserCommand


def create_account(get_create_user):
    account = Blueprint('account', __name__)

    @account.route('/api/v1/account', methods=['post'])
    def create_user_view():
        json = request.get_json()

        command = CreateUserCommand(email=json['email'], password=json['password'])

        create_user = get_create_user()

        create_user.execute(command)

        if not create_user.is_valid:
            return jsonify([n.message for n in create_user.notifications]), 400

        return jsonify('user created'), 201

    return account
