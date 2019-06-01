import unittest
from unittest.mock import Mock, PropertyMock

from flask import Flask
from pyflunt.notifications import Notification

from extra_hours.account.gateways.api.views import init_account_bp


class AccountViewTests(unittest.TestCase):
    def setUp(self):
        self._app = Flask(__name__)

        self._create_user = Mock()
        self._authenticate_user = Mock()
        self._resets_password = Mock()
        self._change_user_password = Mock()

        init_account_bp(self._app,
                        get_create_user=Mock(return_value=self._create_user),
                        get_authenticate_user=Mock(return_value=self._authenticate_user),
                        get_resets_password=Mock(return_value=self._resets_password),
                        get_change_user_password=Mock(return_value=self._change_user_password))

        self._client = self._app.test_client()


class CreateUserViewTests(AccountViewTests):
    def test_should_return_status_code_created_when_use_case_is_valid(self):
        is_valid = PropertyMock(return_value=True)

        type(self._create_user).is_valid = is_valid

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', json=json)

        self.assertEqual(201, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
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

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
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


class AuthenticateUserViewTests(AccountViewTests):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        is_valid = PropertyMock(return_value=True)
        notifications = PropertyMock(return_value=[])
        execute = Mock(return_value='token')

        type(self._authenticate_user).is_valid = is_valid
        type(self._authenticate_user).notifications = notifications
        type(self._authenticate_user).execute = execute

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', json=json)

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_no_authorized_when_use_case_not_is_valid(self):
        user_not_authenticate = Notification('user', 'user not authenticate')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_authenticate])
        execute = Mock(return_value=None)

        type(self._authenticate_user).is_valid = is_valid
        type(self._authenticate_user).notifications = notifications
        type(self._authenticate_user).execute = execute

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', json=json)

        self.assertEqual(401, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        user_not_authenticate = Notification('user', 'user not authenticate')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_authenticate])
        execute = Mock(return_value=None)

        type(self._authenticate_user).is_valid = is_valid
        type(self._authenticate_user).notifications = notifications
        type(self._authenticate_user).execute = execute

        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account/authenticate', json=json)

        self.assertListEqual(['user not authenticate'], response.json)


class ResetsPasswordViewTests(AccountViewTests):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        is_valid = PropertyMock(return_value=True)
        notifications = PropertyMock(return_value=[])

        type(self._resets_password).is_valid = is_valid
        type(self._resets_password).notifications = notifications

        email = 'captain@marvel.com'

        response = self._client.get(f'/api/v1/account/{email}/resets-password')

        self.assertEqual(204, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        email_invalid = Notification('email', 'email invalid')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[email_invalid])

        type(self._resets_password).is_valid = is_valid
        type(self._resets_password).notifications = notifications

        email = 'captain@marvel.com'

        response = self._client.get(f'/api/v1/account/{email}/resets-password')

        self.assertEqual(400, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        email_invalid = Notification('email', 'email invalid')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[email_invalid])

        type(self._resets_password).is_valid = is_valid
        type(self._resets_password).notifications = notifications

        email = 'captain@marvel.com'

        response = self._client.get(f'/api/v1/account/{email}/resets-password')

        self.assertListEqual(['email invalid'], response.json)


class ChangeUserPasswordViewTests(AccountViewTests):
    def test_should_return_status_no_content_when_use_case_is_valid(self):
        email = 'captain@marvel.com'

        json = {
            'old_password': 'test123456',
            'new_password': 'test654321',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', json=json)

        self.assertEqual(204, response.status_code)

    def test_should_return_status_bad_request_when_use_case_not_is_valid(self):
        user_not_authenticate = Notification('user', 'user not authenticate')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_authenticate])

        type(self._change_user_password).is_valid = is_valid
        type(self._change_user_password).notifications = notifications

        email = 'captain@marvel.com'

        json = {
            'old_password': '',
            'new_password': '',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', json=json)

        self.assertEqual(400, response.status_code)

    def test_should_return_status_list_of_notification_when_use_case_not_is_valid(self):
        user_not_authenticate = Notification('user', 'user not authenticate')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_authenticate])

        type(self._change_user_password).is_valid = is_valid
        type(self._change_user_password).notifications = notifications

        email = 'captain@marvel.com'

        json = {
            'old_password': '',
            'new_password': '',
        }

        response = self._client.post(f'/api/v1/account/{email}/change-password', json=json)

        self.assertListEqual(['user not authenticate'], response.json)
