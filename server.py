from datetime import datetime
from fastapi import FastAPI, Header

from extra_hours.account.gateways.api.views import init_account
from extra_hours.account.gateways.infra import repositories as account_repositories
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.use_case import CreateUser, AuthenticateUser, ResetsPassword, ChangeUserPassword
from extra_hours.billing.gateways.api.views import init_billing
from extra_hours.billing.gateways.infra import repositories as billing_repositories
from extra_hours.billing.use_case import CreateBilling, ConfirmReceiveBilling, CancelReceiveBilling, UpdateBilling
from extra_hours.shared.gateways.infra.uow import Uow


class Config:
    CONNECTION_STRING = 'sqlite:///db.sqlite3'
    SECRET_KEY = '9BADBE64EE76C9EB87559BE2DB48F'


def get_user(authorization=Header(None)):
    token_service = JwtTokenService(Config.SECRET_KEY)
    user = token_service.decode(authorization)
    return user or {}


app = FastAPI(title='Extra Hours', version='v1')

uow = Uow(Config.CONNECTION_STRING)


def get_create_user():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow.session)
    return CreateUser(user_repository=user_repository)


def get_authenticate_user():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow.session)
    token_service = JwtTokenService(Config.SECRET_KEY)
    return AuthenticateUser(user_repository=user_repository, token_service=token_service)


def get_resets_password():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow.session)
    return ResetsPassword(user_repository=user_repository)


def get_change_user_password():
    user_repository = account_repositories.SqlAlchemyUserRepository(uow.session)
    return ChangeUserPassword(user_repository=user_repository)


init_account(app,
             uow=uow,
             get_create_user=get_create_user,
             get_authenticate_user=get_authenticate_user,
             get_resets_password=get_resets_password,
             get_change_user_password=get_change_user_password)


def get_create_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow.session)
    return CreateBilling(user_repository=user_repository)


def get_confirm_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow.session)
    return ConfirmReceiveBilling(user_repository=user_repository)


def get_cancel_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow.session)
    return CancelReceiveBilling(user_repository=user_repository)


def get_update_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository(uow.session)
    return UpdateBilling(user_repository=user_repository)


init_billing(app,
             uow=uow,
             get_create_billing=get_create_billing,
             get_confirm_receive_billing=get_confirm_receive_billing,
             get_cancel_receive_billing=get_cancel_receive_billing,
             get_update_billing=get_update_receive_billing,
             get_user=get_user)


@app.get('/')
def index():
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {'data': data, 'errors': []}
