from flask import Blueprint, request, Response

from extra_hours.account.commands import CreateUserCommand


def create_account(app):
    account = Blueprint('account', __name__)

    @account.route('/api/v1/account', methods=['post'])
    def create_user():
        json = request.get_json()

        command = CreateUserCommand(email=json['email'], password=json['password'])

        use_case = app.config.get('CREATE_USER')

        use_case.execute(command)

        return Response(status=201)

    return account
