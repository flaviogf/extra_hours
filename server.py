from fastapi import FastAPI, Header

from extra_hours.account.gateways.api.views import init_account
from extra_hours.account.gateways.infra import repositories as account_repositories
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.use_case import CreateUser, AuthenticateUser, ResetsPassword, ChangeUserPassword
from extra_hours.billing.gateways.api.views import init_billing
from extra_hours.billing.gateways.infra import repositories as billing_repositories
from extra_hours.billing.use_case import CreateBilling, ConfirmReceiveBilling, CancelReceiveBilling, UpdateBilling


def get_user(authorization=Header(None)):
    return {'uid': authorization}


app = FastAPI(title='Extra Hours', version='v1')


def get_create_user():
    user_repository = account_repositories.SqlAlchemyUserRepository()
    return CreateUser(user_repository=user_repository)


def get_authenticate_user():
    user_repository = account_repositories.SqlAlchemyUserRepository()
    token_service = JwtTokenService()
    return AuthenticateUser(user_repository=user_repository, token_service=token_service)


def get_resets_password():
    user_repository = account_repositories.SqlAlchemyUserRepository()
    return ResetsPassword(user_repository=user_repository)


def get_change_user_password():
    user_repository = account_repositories.SqlAlchemyUserRepository()
    return ChangeUserPassword(user_repository=user_repository)


init_account(app,
             get_create_user=get_create_user,
             get_authenticate_user=get_authenticate_user,
             get_resets_password=get_resets_password,
             get_change_user_password=get_change_user_password)


def get_create_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository()
    return CreateBilling(user_repository=user_repository)


def get_confirm_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository()
    return ConfirmReceiveBilling(user_repository=user_repository)


def get_cancel_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository()
    return CancelReceiveBilling(user_repository=user_repository)


def get_update_receive_billing():
    user_repository = billing_repositories.SqlAlchemyUserRepository()
    return UpdateBilling(user_repository=user_repository)


init_billing(app,
             get_create_billing=get_create_billing,
             get_confirm_receive_billing=get_confirm_receive_billing,
             get_cancel_receive_billing=get_cancel_receive_billing,
             get_update_billing=get_update_receive_billing,
             get_user=get_user)
