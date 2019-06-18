from pydantic import BaseModel
from starlette.responses import Response

from extra_hours.account.commands import (AuthenticateUserCommand,
                                          CreateUserCommand,
                                          ResetsPasswordCommand,
                                          ChangeUserPasswordCommand)


class CreateUserModel(BaseModel):
    email: str = ''
    password: str = ''


class AuthenticateUserModel(BaseModel):
    email: str = ''
    password: str = ''


class ChangePasswordModel(BaseModel):
    old_password: str = ''
    new_password: str = ''


def init_account(app, **kwargs):
    uow = kwargs.get('uow')
    get_create_user = kwargs.get('get_create_user')
    get_authenticate_user = kwargs.get('get_authenticate_user')
    get_resets_password = kwargs.get('get_resets_password')
    get_change_user_password = kwargs.get('get_change_user_password')

    @app.post('/api/v1/account', tags=['account'])
    def create_user(model: CreateUserModel, response: Response):
        with uow():
            command = CreateUserCommand(email=model.email,
                                        password=model.password)

            use_case = get_create_user()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'user created', 'errors': []}

    @app.post('/api/v1/account/authenticate', tags=['account'])
    def authenticate_user(model: AuthenticateUserModel, response: Response):
        with uow():
            use_case = get_authenticate_user()

            command = AuthenticateUserCommand(email=model.email,
                                              password=model.password)

            token = use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 401

                return {'data': None, 'errors': errors}

            return {'data': token, 'errors': []}

    @app.post('/api/v1/account/{email}/resets-password', tags=['account'])
    def resets_password(email: str, response: Response):
        with uow():
            command = ResetsPasswordCommand(email=email)

            use_case = get_resets_password()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'password resets', 'errors': []}

    @app.post('/api/v1/account/{email}/change-password', tags=['account'])
    def change_user_password(model: ChangePasswordModel, email: str, response: Response):
        with uow():
            command = ChangeUserPasswordCommand(email=email,
                                                old_password=model.old_password,
                                                new_password=model.new_password)

            use_case = get_change_user_password()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'password changed', 'errors': []}
