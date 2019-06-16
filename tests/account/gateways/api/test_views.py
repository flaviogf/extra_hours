import json
import unittest
from unittest.mock import Mock, PropertyMock

from fastapi import FastAPI
from pyflunt.notifications import Notification
from starlette.testclient import TestClient

from extra_hours.account.gateways.api.views import init_account


class AccountViewTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()

        self._create_user = Mock()
        self._authenticate_user = Mock()
        self._resets_password = Mock()
        self._change_user_password = Mock()

        init_account(app,
                     get_create_user=Mock(return_value=self._create_user),
                     get_authenticate_user=Mock(return_value=self._authenticate_user),
                     get_resets_password=Mock(return_value=self._resets_password),
                     get_change_user_password=Mock(return_value=self._change_user_password))

        self._client = TestClient(app)


class CreateUserViewTests(AccountViewTests):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        invalid_name = Notification('name', 'invalid name')

        type(self._create_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_user).notifications = PropertyMock(return_value=[invalid_name])

        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        invalid_name = Notification('name', 'invalid name')

        type(self._create_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_user).notifications = PropertyMock(return_value=[invalid_name])

        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', data=json.dumps(data))

        result = response.json()['errors']

        expected = ['invalid name']

        self.assertListEqual(expected, result)


class AuthenticateUserViewTests(AccountViewTests):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        token = 'token'

        type(self._authenticate_user).execute = Mock(return_value=token)

        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_no_authorized_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_authenticate = Notification('user', 'user not authenticate')

        type(self._authenticate_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._authenticate_user).notifications = PropertyMock(return_value=[user_not_authenticate])

        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', data=json.dumps(data))

        self.assertEqual(401, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_authenticate = Notification('user', 'user not authenticate')

        type(self._authenticate_user).is_valid = PropertyMock(return_value=is_valid)
        type(self._authenticate_user).notifications = PropertyMock(return_value=[user_not_authenticate])

        data = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', data=json.dumps(data))

        result = response.json()['errors']

        expected = ['user not authenticate']

        self.assertListEqual(expected, result)


class ResetsPasswordViewTests(AccountViewTests):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        email = 'captain@marvel.com'

        response = self._client.post(f'/api/v1/account/{email}/resets-password')

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        email_invalid = Notification('email', 'email invalid')

        type(self._resets_password).is_valid = PropertyMock(return_value=is_valid)
        type(self._resets_password).notifications = PropertyMock(return_value=[email_invalid])

        email = 'captain@marvel.com'

        response = self._client.post(f'/api/v1/account/{email}/resets-password')

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        email_invalid = Notification('email', 'email invalid')

        type(self._resets_password).is_valid = PropertyMock(return_value=is_valid)
        type(self._resets_password).notifications = PropertyMock(return_value=[email_invalid])

        email = 'captain@marvel.com'

        response = self._client.post(f'/api/v1/account/{email}/resets-password')

        result = response.json()['errors']

        expected = ['email invalid']

        self.assertListEqual(expected, result)


class ChangeUserPasswordViewTests(AccountViewTests):
    def test_should_return_status_ok_when_use_case_is_valid(self):
        email = 'captain@marvel.com'

        data = {
            'old_password': 'test123456',
            'new_password': 'test654321',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_return_status_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_authenticate = Notification('user', 'user not authenticate')

        type(self._change_user_password).is_valid = PropertyMock(return_value=is_valid)
        type(self._change_user_password).notifications = PropertyMock(return_value=[user_not_authenticate])

        email = 'captain@marvel.com'

        data = {
            'old_password': '',
            'new_password': '',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_authenticate = Notification('user', 'user not authenticate')

        type(self._change_user_password).is_valid = PropertyMock(return_value=is_valid)
        type(self._change_user_password).notifications = PropertyMock(return_value=[user_not_authenticate])

        email = 'captain@marvel.com'

        data = {
            'old_password': '',
            'new_password': '',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', data=json.dumps(data))

        result = response.json()['errors']

        expected = ['user not authenticate']

        self.assertListEqual(expected, result)
