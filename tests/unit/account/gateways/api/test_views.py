import json
import unittest
from contextlib import contextmanager
from unittest.mock import Mock, PropertyMock

from pyflunt.notifications import Notification
from sanic import Sanic
from sanic.testing import SanicTestClient

from extra_hours.account.gateways.api.views import init_account


@contextmanager
def fake_uow():
    yield


class AccountTestCase(unittest.TestCase):
    def setUp(self):
        app = Sanic()

        self._create_user = Mock()

        init_account(app=app,
                     uow=fake_uow,
                     get_create_user=Mock(return_value=self._create_user))

        self._client = SanicTestClient(app, port=None)


class CreateUserTests(AccountTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        data = {
            'email': 'naruto@uzumaki.com',
            'password': 'sasuke123'
        }

        _, response = self._client.post('/api/v1/account', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        email_not_is_valid = Notification('email', 'email not is valid')

        type(self._create_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_user).notifications = PropertyMock(return_value=[email_not_is_valid])

        data = {
            'email': 'naruto@uzumaki.com',
            'password': 'sasuke123'
        }

        _, response = self._client.post('/api/v1/account', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        email_not_is_valid = Notification('email', 'email not is valid')

        type(self._create_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_user).notifications = PropertyMock(return_value=[email_not_is_valid])

        data = {
            'email': 'naruto@uzumaki.com',
            'password': 'sasuke123'
        }

        _, response = self._client.post('/api/v1/account', data=json.dumps(data))

        result = response.json['errors']

        expected = ['email not is valid']

        self.assertListEqual(expected, result)
