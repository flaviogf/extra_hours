from collections import defaultdict
from datetime import datetime
from functools import wraps
from os import getenv

from sanic import Sanic
from sanic.response import json

from extra_hours.account.gateways.api.views import init_account
from extra_hours.account.gateways.infra import repositories as account_repositories
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.use_cases import CreateUser, AuthenticateUser, ChangeUserPassword
from extra_hours.billing.gateways.api.views import init_billing
from extra_hours.billing.gateways.infra import repositories as billing_repositories
from extra_hours.billing.use_cases import AddBilling, ConfirmReceiveBilling, CancelReceiveBilling, RemoveBilling, \
    UpdateBilling
from extra_hours.shared.gateways.infra.uow import Uow


class Config:
    DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SECRET_KEY = getenv('SECRET_KEY', '44B2C4D4CFA5569485BD86C8F5BC1')


app = Sanic()

uow = Uow(connection_string=Config.DATABASE_URL, echo=True)


def authorized():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(request, *args, **kwargs):
            token_service = JwtTokenService(Config.SECRET_KEY)
            token = request.token
            user = token_service.decode(token)
            user = user or defaultdict(str)
            return fn(request, user, *args, **kwargs)

        return wrapper

    return decorator


def get_create_user():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow)
    return CreateUser(user_repository)


def get_authenticate_user():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow)
    token_service = JwtTokenService(Config.SECRET_KEY)
    return AuthenticateUser(user_repository, token_service)


def get_change_user_password():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow)
    return ChangeUserPassword(user_repository)


init_account(app=app,
             uow=uow,
             get_create_user=get_create_user,
             get_authenticate_user=get_authenticate_user,
             get_change_user_password=get_change_user_password)


def get_add_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow)
    return AddBilling(user_repository)


def get_confirm_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow)
    return ConfirmReceiveBilling(user_repository)


def get_cancel_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow)
    return CancelReceiveBilling(user_repository)


def get_remove_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow)
    return RemoveBilling(user_repository)


def get_update_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow)
    return UpdateBilling(user_repository)


init_billing(app=app,
             uow=uow,
             authorized=authorized,
             user_repository=billing_repositories.SqlAlchemyUserRepository(uow),
             get_add_billing=get_add_billing,
             get_confirm_receive_billing=get_confirm_receive_billing,
             get_cancel_receive_billing=get_cancel_receive_billing,
             get_remove_billing=get_remove_billing,
             get_update_billing=get_update_billing)


@app.get('/')
def status(request):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return json(body={'data': data, 'errors': []}, headers={'ip': request.ip})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
