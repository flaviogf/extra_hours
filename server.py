from datetime import datetime
from os import getenv

from sanic import Sanic
from sanic.response import json

from extra_hours.account.gateways.api.views import init_account
from extra_hours.account.gateways.infra.repositories import SqlAlchemyUserRepository
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.use_cases import CreateUser, AuthenticateUser
from extra_hours.shared.gateways.infra.uow import Uow


class Config:
    DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SECRET_KEY = getenv('SECRET_KEY', '44B2C4D4CFA5569485BD86C8F5BC1')


app = Sanic()

uow = Uow(connection_string=Config.DATABASE_URL, echo=True)


def get_create_user():
    user_repository = SqlAlchemyUserRepository(uow)
    return CreateUser(user_repository)


def get_authenticate_user():
    user_repository = SqlAlchemyUserRepository(uow)
    token_service = JwtTokenService(Config.SECRET_KEY)
    return AuthenticateUser(user_repository, token_service)


init_account(app=app,
             uow=uow,
             get_create_user=get_create_user,
             get_authenticate_user=get_authenticate_user)


@app.get('/')
def status(request):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return json(body={'data': data, 'errors': []}, headers={'ip': request.ip})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
