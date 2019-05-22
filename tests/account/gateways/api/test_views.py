import unittest
from unittest.mock import PropertyMock, MagicMock

from flask import Flask
from pyflunt.notifications import Notification

from extra_hours.account.gateways.api.views import create_account


class AccountTests(unittest.TestCase):
    def setUp(self):
        self._app = Flask(__name__)

        self._create_user = MagicMock()

        account = create_account(MagicMock(return_value=self._create_user))

        self._app.register_blueprint(account)

        self._client = self._app.test_client()

    def test_should_create_billing_return_status_code_ok_when_use_case_is_valid(self):
        is_valid = PropertyMock(return_value=True)

        type(self._create_user).is_valid = is_valid

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', json=json)

        self.assertEqual(201, response.status_code)

    def test_should_create_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        invalid_name = Notification('name', 'invalid name')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[invalid_name])

        type(self._create_user).is_valid = is_valid
        type(self._create_user).notifications = notifications

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', json=json)

        self.assertEqual(400, response.status_code)

    def test_should_create_billing_return_list_of_notifications_when_use_case_not_is_valid(self):
        invalid_name = Notification('name', 'invalid name')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[invalid_name])

        type(self._create_user).is_valid = is_valid
        type(self._create_user).notifications = notifications

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', json=json)

        self.assertListEqual(['invalid name'], response.json)
