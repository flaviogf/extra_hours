from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

from sanic.response import json

from extra_hours.billing.commands import AddBillingCommand, ConfirmReceiveBillingCommand, CancelReceiveBillingCommand


def init_billing(**kwargs):
    app = kwargs.get('app')
    uow = kwargs.get('uow')
    authorized = kwargs.get('authorized')
    user_repository = kwargs.get('user_repository')
    get_add_billing = kwargs.get('get_add_billing')
    get_confirm_receive_billing = kwargs.get('get_confirm_receive_billing')
    get_cancel_receive_billing = kwargs.get('get_cancel_receive_billing')

    @app.post('/api/v1/billing')
    @authorized()
    def add_billing(request, user):
        with uow():
            work_date = request.json.get('work_date')
            work_date = datetime.strptime(work_date, '%Y-%m-%d %H:%M:%S') if work_date else datetime.now()

            value = request.json.get('value')
            value = Decimal(value)

            command = AddBillingCommand(user_uid=user.get('uid', ''),
                                        title=request.json.get('title', ''),
                                        description=request.json.get('description', ''),
                                        value=value,
                                        work_date=work_date)

            use_case = get_add_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                return json(body={'data': None, 'errors': errors}, status=400)

            return json(body={'data': asdict(command), 'errors': []})

    @app.post('/api/v1/billing/<billing_uid>/confirm-receive')
    @authorized()
    def confirm_receive_billing(request, user, billing_uid):
        with uow():
            command = ConfirmReceiveBillingCommand(user_uid=user.get('uid'),
                                                   billing_uid=billing_uid)

            use_case = get_confirm_receive_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                return json(body={'data': None, 'errors': errors}, status=400)

            return json(body={'data': asdict(command), 'errors': []})

    @app.post('/api/v1/billing/<billing_uid>/cancel-receive')
    @authorized()
    def cancel_receive_billing(request, user, billing_uid):
        with uow():
            command = CancelReceiveBillingCommand(user_uid=user.get('uid'),
                                                  billing_uid=billing_uid)

            use_case = get_cancel_receive_billing()

            use_case.execute(command)

            if not use_case.is_valid:
                errors = [n.message for n in use_case.notifications]

                return json(body={'data': None, 'errors': errors}, status=400)

            return json(body={'data': asdict(command), 'errors': []})

    @app.get('/api/v1/billing/received')
    @authorized()
    def list_received(request, user):
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)

        billing = user_repository.list_billing_received(user.get('uid'), limit=limit, offset=offset)

        return json(body={'data': billing, 'errors': []})

    @app.get('/api/v1/billing/not-received')
    @authorized()
    def list_not_received(request, user):
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)

        billing = user_repository.list_billing_not_received(user.get('uid'), limit=limit, offset=offset)

        return json(body={'data': billing, 'errors': []})
