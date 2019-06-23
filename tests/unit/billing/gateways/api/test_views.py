import json
import unittest
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from unittest.mock import Mock, PropertyMock

from pyflunt.notifications import Notification
from sanic import Sanic
from sanic.testing import SanicTestClient

from extra_hours.billing.gateways.api.views import init_billing


@contextmanager
def fake_uow():
    yield


class BillingTestCase(unittest.TestCase):
    def setUp(self):
        app = Sanic()

        self._add_billing = Mock()

        init_billing(app=app,
                     uow=fake_uow,
                     get_add_billing=Mock(return_value=self._add_billing))

        self._client = SanicTestClient(app, port=None)


class AddBillingTests(BillingTestCase):
    def test_should_add_billing_return_status_code_ok_when_use_case_is_valid(self):
        yesterday = datetime.now() + timedelta(days=1)

        data = {
            'user_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'Yesterday',
            'value': 10,
            'work_date': yesterday.strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.post('/api/v1/billing', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_add_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        wrong_password = Notification('title', 'title should be inform')

        type(self._add_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._add_billing).notifications = PropertyMock(return_value=[wrong_password])

        yesterday = datetime.now() + timedelta(days=1)

        data = {
            'user_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'Yesterday',
            'value': 10,
            'work_date': yesterday.strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.post('/api/v1/billing', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_add_billing_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        wrong_password = Notification('title', 'title should be inform')

        type(self._add_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._add_billing).notifications = PropertyMock(return_value=[wrong_password])

        yesterday = datetime.now() + timedelta(days=1)

        data = {
            'user_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'Yesterday',
            'value': 10,
            'work_date': yesterday.strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.post('/api/v1/billing', data=json.dumps(data))

        result = response.json['errors']

        expected = ['title should be inform']

        self.assertListEqual(expected, result)
