from dataclasses import asdict

from sanic.response import json

from extra_hours.account.commands import CreateUserCommand


def init_account(**kwargs):
    app = kwargs.get('app')
    uow = kwargs.get('uow')
    get_create_user = kwargs.get('get_create_user')

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
