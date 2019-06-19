from datetime import datetime

from fastapi import Depends
from pydantic import BaseModel
from starlette.responses import Response

from extra_hours.billing.commands import (CreateBillingCommand,
                                          ConfirmReceiveBillingCommand,
                                          CancelReceiveBillingCommand,
                                          UpdateBillingCommand)


class CreateBillingModel(BaseModel):
    title: str = ''
    description: str = ''
    value: float = 0.0
    work_date: datetime = None


class UpdateBillingModel(BaseModel):
    title: str = ''
    description: str = ''
    value: float = 0.0
    work_date: datetime = None


def init_billing(app, **kwargs):
    uow = kwargs.get('uow')
    get_create_billing = kwargs.get('get_create_billing')
    get_confirm_receive_billing = kwargs.get('get_confirm_receive_billing')
    get_cancel_receive_billing = kwargs.get('get_cancel_receive_billing')
    get_update_billing = kwargs.get('get_update_billing')
    get_user = kwargs.get('get_user')

    @app.post('/api/v1/billing', tags=['billing'])
    def create_billing(model: CreateBillingModel, response: Response, user=Depends(get_user)):
        with uow():
            command = CreateBillingCommand(user_id=user.get('uid', ''),
                                           title=model.title,
                                           description=model.description,
                                           value=model.value,
                                           work_date=model.work_date)

            use_case = get_create_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'billing created', 'errors': []}

    @app.post('/api/v1/billing/{billing_id}/confirm-receive', tags=['billing'])
    def confirm_receive_billing(billing_id: str, response: Response, user=Depends(get_user)):
        with uow():
            command = ConfirmReceiveBillingCommand(user_id=user.get('uid', ''), billing_id=billing_id)

            use_case = get_confirm_receive_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'billing received confirmed', 'errors': []}

    @app.post('/api/v1/billing/{billing_id}/cancel-receive', tags=['billing'])
    def cancel_receive_billing(billing_id: str, response: Response, user=Depends(get_user)):
        with uow():
            command = CancelReceiveBillingCommand(user_id=user.get('uid', ''), billing_id=billing_id)

            use_case = get_cancel_receive_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'billing received canceled', 'errors': []}

    @app.put('/api/v1/billing/{billing_id}', tags=['billing'])
    def update_billing(model: UpdateBillingModel, billing_id: str, response: Response, user=Depends(get_user)):
        with uow():
            command = UpdateBillingCommand(user_id=user.get('uid', ''),
                                           billing_id=billing_id,
                                           title=model.title,
                                           description=model.description,
                                           value=model.value,
                                           work_date=model.work_date)

            use_case = get_update_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                response.status_code = 400

                return {'data': None, 'errors': errors}

            return {'data': 'billing updated', 'errors': []}
