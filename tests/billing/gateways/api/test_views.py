import json
import unittest
import uuid
from contextlib import contextmanager
from datetime import datetime
from unittest.mock import Mock, PropertyMock

from fastapi import FastAPI
from pyflunt.notifications import Notification
from starlette.testclient import TestClient

from extra_hours.billing.gateways.api.views import init_billing
from extra_hours.billing.queries import BillingListQueryResult

FAKE_BILLING_LIST_QUERY_RESULT = [BillingListQueryResult(uid=str(uuid.uuid4()),
                                                         title='gas station',
                                                         description='yesterday',
                                                         value=100.99,
                                                         work_date='2019-10-10 10:10',
                                                         received_date='2019-10-10 10:20',
                                                         user_uid=str(uuid.uuid4()))]


@contextmanager
def fake_uow():
    yield


def fake_get_user():
    return {'uid': str(uuid.uuid4())}


class BillingTestCase(unittest.TestCase):
    def setUp(self):
        app = FastAPI()

        self._create_billing = Mock()
        self._confirm_receive_billing = Mock()
        self._cancel_receive_billing = Mock()
        self._update_billing = Mock()
        self._user_repository = Mock()

        init_billing(app,
                     uow=fake_uow,
                     user_repository=self._user_repository,
                     get_create_billing=Mock(return_value=self._create_billing),
                     get_confirm_receive_billing=Mock(return_value=self._confirm_receive_billing),
                     get_cancel_receive_billing=Mock(return_value=self._cancel_receive_billing),
                     get_update_billing=Mock(return_value=self._update_billing),
                     get_user=fake_get_user)

        self._client = TestClient(app)


class CreateBillingTests(BillingTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        today = datetime.today().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        response = self._client.post('/api/v1/billing', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._create_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_billing).notifications = PropertyMock(return_value=[user_not_exists])

        today = datetime.today().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        response = self._client.post('/api/v1/billing', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._create_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._create_billing).notifications = PropertyMock(return_value=[user_not_exists])

        today = datetime.today().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 299.99,
            'work_date': today
        }

        response = self._client.post('/api/v1/billing', data=json.dumps(data))

        result = response.json()['errors']

        expected = ['user not exists']

        self.assertListEqual(expected, result)


class ConfirmReceiveBillingTests(BillingTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive')

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._confirm_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._confirm_receive_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive')

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._confirm_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._confirm_receive_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/confirm-receive')

        result = response.json()['errors']

        expected = ['user not exists']

        self.assertListEqual(expected, result)


class CancelReceiveBillingTests(BillingTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive')

        self.assertEqual(200, response.status_code)

    def test_should_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._cancel_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._cancel_receive_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive')

        self.assertEqual(400, response.status_code)

    def test_should_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._cancel_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._cancel_receive_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        response = self._client.post(f'/api/v1/billing/{billing_id}/cancel-receive')

        result = response.json()['errors']

        expected = ['user not exists']

        self.assertListEqual(expected, result)


class UpdateBillingTests(BillingTestCase):
    def test_should_return_status_code_ok_when_use_case_is_valid(self):
        billing_id = uuid.uuid4()

        work_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        response = self._client.put(f'/api/v1/billing/{str(billing_id)}', json=data)

        self.assertEqual(200, response.status_code)

    def test_should_return_status_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._update_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._update_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        work_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        response = self._client.put(f'/api/v1/billing/{str(billing_id)}', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_return_list_of_notifications_when_use_case_not_is_valid(self):
        is_valid = False
        user_not_exists = Notification('user', 'user not exists')

        type(self._update_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._update_billing).notifications = PropertyMock(return_value=[user_not_exists])

        billing_id = uuid.uuid4()

        work_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        data = {
            'title': 'gas station',
            'description': 'before today',
            'value': 250.99,
            'work_date': work_date
        }

        response = self._client.put(f'/api/v1/billing/{str(billing_id)}', data=json.dumps(data))

        result = response.json()['errors']

        expected = ['user not exists']

        self.assertListEqual(expected, result)


class ListReceivedBillingTests(BillingTestCase):
    def setUp(self):
        super().setUp()

        self._user_repository.list_received_billing_list_query_result.return_value = FAKE_BILLING_LIST_QUERY_RESULT

    def test_should_list_received_billing_return_status_code_ok(self):
        response = self._client.get('/api/v1/billing/received')

        self.assertEqual(200, response.status_code)

    def test_should_list_received_billing_return_billing_list_query_result_list(self):
        response = self._client.get('/api/v1/billing/received')

        result = response.json()['data']

        self.assertEqual(1, len(result))

        for it in result:
            with self.subTest():
                self.assertIsInstance(it, dict)


class ListNotReceivedBillingTests(BillingTestCase):
    def setUp(self):
        super().setUp()

        self._user_repository.list_not_received_billing_list_query_result.return_value = FAKE_BILLING_LIST_QUERY_RESULT

    def test_should_list_not_received_billing_return_status_code_ok(self):
        response = self._client.get('/api/v1/billing/not-received')

        self.assertEqual(200, response.status_code)

    def test_should_list_not_received_billing_return_billing_list_query_result_list(self):
        response = self._client.get('/api/v1/billing/not-received')

        result = response.json()['data']

        self.assertEqual(1, len(result))

        for it in result:
            with self.subTest():
                self.assertIsInstance(it, dict)
