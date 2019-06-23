from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

from sanic.response import json

from extra_hours.billing.commands import AddBillingCommand


def init_billing(**kwargs):
    app = kwargs.get('app')
    uow = kwargs.get('uow')
    get_add_billing = kwargs.get('get_add_billing')

    @app.post('/api/v1/billing')
    def add_billing(request):
        with uow():
            work_date = request.json.get('work_date')
            work_date = datetime.strptime(work_date, '%Y-%m-%d %H:%M:%S') if work_date else datetime.now()

            value = request.json.get('value')
            value = Decimal(value) if str(value).isnumeric() else Decimal(0)

            command = AddBillingCommand(user_uid=request.json.get('user_uid', ''),
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
