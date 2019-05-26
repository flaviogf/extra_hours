import unittest
import uuid
from datetime import datetime
from unittest.mock import Mock, PropertyMock

from flask import Flask
from pyflunt.notifications import Notification

from extra_hours.billing.gateways.api.views import create_billing_bp


class CreateBillingView(unittest.TestCase):
    def setUp(self):
        self._create_billing = Mock()

        self._billing_bp = create_billing_bp(Mock(return_value=self._create_billing))

        self._app = Flask(__name__)

        self._app.register_blueprint(self._billing_bp)

        self._client = self._app.test_client()

    def test_should_return_status_code_created_when_use_case_is_valid(self):
        today = datetime.today().strftime('%Y-%m-%d')

        json = {
            'user_id': str(uuid.uuid4()),
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

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
            'user_id': str(uuid.uuid4()),
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

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
            'user_id': str(uuid.uuid4()),
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        response = self._client.post('/api/v1/billing', json=json)

        self.assertListEqual(['user not exists'], response.json)
