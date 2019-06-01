import unittest
import uuid
from datetime import datetime
from unittest.mock import Mock, PropertyMock

from flask import Flask, g
from pyflunt.notifications import Notification

from extra_hours.billing.gateways.api.views import init_billing_bp


class BillingViewTestCase(unittest.TestCase):
    def setUp(self):
        self._app = Flask(__name__)

        self._create_billing = Mock()
        self._confirm_receive_billing = Mock()
        self._cancel_receive_billing = Mock()
        self._update_billing = Mock()

        init_billing_bp(self._app,
                        get_create_billing=Mock(return_value=self._create_billing),
                        get_confirm_receive_billing=Mock(return_value=self._confirm_receive_billing),
                        get_cancel_receive_billing=Mock(return_value=self._cancel_receive_billing),
                        get_update_billing=Mock(return_value=self._update_billing))

        self._client = self._app.test_client()

    def _set_user(self):
        g.user = {
            'uid': str(uuid.uuid4()),
            'email': 'peter@email.com'
        }


class CreateBillingView(BillingViewTestCase):
    def test_should_return_status_code_created_when_use_case_is_valid(self):
        today = datetime.today().strftime('%Y-%m-%d')

        json = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post('/api/v1/billing', json=json)

            self.assertEqual(201, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._create_billing).is_valid = is_valid
        type(self._create_billing).notifications = notifications

        today = datetime.today().strftime('%Y-%m-%d')

        json = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post('/api/v1/billing', json=json)

            self.assertEqual(400, response.status_code)

    def test_should_return_a_list_of_notifications_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._create_billing).is_valid = is_valid
        type(self._create_billing).notifications = notifications

        today = datetime.today().strftime('%Y-%m-%d')

        json = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post('/api/v1/billing', json=json)

            self.assertListEqual(['user not exists'], response.json)


class ConfirmReceiveBillingView(BillingViewTestCase):
    def test_should_return_status_code_no_content_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()

        json = {'billing_id': billing_id}

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive', json=json)

            self.assertEqual(204, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._confirm_receive_billing).is_valid = is_valid
        type(self._confirm_receive_billing).notifications = notifications

        billing_id = uuid.uuid4()

        json = {'billing_id': billing_id}

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive', json=json)

            self.assertEqual(400, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._confirm_receive_billing).is_valid = is_valid
        type(self._confirm_receive_billing).notifications = notifications

        billing_id = uuid.uuid4()

        json = {'billing_id': billing_id}

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive', json=json)

            self.assertListEqual(['user not exists'], response.json)


class CancelReceiveBillingView(BillingViewTestCase):
    def test_should_return_status_code_no_content_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()

        json = {
            'billing_id': billing_id,
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive', json=json)

            self.assertEqual(204, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._cancel_receive_billing).is_valid = is_valid
        type(self._cancel_receive_billing).notifications = notifications

        billing_id = uuid.uuid4()

        json = {
            'billing_id': billing_id,
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive', json=json)

            self.assertEqual(400, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._cancel_receive_billing).is_valid = is_valid
        type(self._cancel_receive_billing).notifications = notifications

        billing_id = uuid.uuid4()

        json = {
            'billing_id': billing_id,
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive', json=json)

            self.assertListEqual(['user not exists'], response.json)


class UpdateBillingViewTests(BillingViewTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()
        work_date = datetime.now().strftime('%Y-%m-%d')

        json = {
            'billing_id': str(billing_id),
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.put(f'/api/v1/billing/{billing_id}', json=json)

            self.assertEqual(204, response.status_code)

    def test_should_return_status_bad_request_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._update_billing).is_valid = is_valid
        type(self._update_billing).notifications = notifications

        billing_id = uuid.uuid4()
        work_date = datetime.now().strftime('%Y-%m-%d')

        json = {
            'billing_id': str(billing_id),
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.put(f'/api/v1/billing/{billing_id}', json=json)

            self.assertEqual(400, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        user_not_exists = Notification('user', 'user not exists')

        is_valid = PropertyMock(return_value=False)
        notifications = PropertyMock(return_value=[user_not_exists])

        type(self._update_billing).is_valid = is_valid
        type(self._update_billing).notifications = notifications

        billing_id = uuid.uuid4()
        work_date = datetime.now().strftime('%Y-%m-%d')

        json = {
            'billing_id': str(billing_id),
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        with self._app.app_context():
            self._set_user()

            response = self._client.put(f'/api/v1/billing/{billing_id}', json=json)

            self.assertListEqual(['user not exists'], response.json)
