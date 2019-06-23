from dataclasses import asdict

from sanic.response import json

from extra_hours.account.commands import CreateUserCommand, AuthenticateUserCommand, ChangeUserPasswordCommand


def init_account(**kwargs):
    app = kwargs.get('app')
    uow = kwargs.get('uow')
    get_create_user = kwargs.get('get_create_user')
    get_authenticate_user = kwargs.get('get_authenticate_user')
    get_change_user_password = kwargs.get('get_change_user_password')

    @app.post('/api/v1/account')
    def create_account(request):
        with uow():
            command = CreateUserCommand(email=request.json.get('email', ''),
                                        password=request.json.get('password', ''))

            use_case = get_create_user()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                return json(body={'data': None, 'errors': errors}, status=400)

            return json(body={'data': asdict(command), 'errors': []})

    @app.post('/api/v1/account/authenticate')
    def authenticate_user(request):
        command = AuthenticateUserCommand(email=request.json.get('email', ''),
                                          password=request.json.get('password', ''))

        use_case = get_authenticate_user()

        use_case.execute(command)

        if not use_case.is_valid:
            errors = [n.message for n in use_case.notifications]

            return json(body={'data': None, 'errors': errors}, status=400)

        return json(body={'data': asdict(command), 'errors': []})

    @app.post('/api/v1/account/change-password')
    def change_user_password(request):
        command = ChangeUserPasswordCommand(email=request.json.get('email'),
                                            old_password=request.json.get('old_password'),
                                            new_password=request.json.get('new_password'))

        use_case = get_change_user_password()

        use_case.execute(command)

        if not use_case.is_valid:
            errors = [n.message for n in use_case.notifications]

            return json(body={'data': None, 'errors': errors}, status=400)

        return json(body={'data': asdict(command), 'errors': []})
