import json
import unittest
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from decimal import Decimal
from functools import wraps
from unittest.mock import Mock, PropertyMock

from pyflunt.notifications import Notification
from sanic import Sanic
from sanic.testing import SanicTestClient

from extra_hours.billing.gateways.api.views import init_billing
from extra_hours.billing.queries import BillingListQueryResult

FAKE_BILLING_LIST_QUERY_RESULT = BillingListQueryResult(uid=str(uuid.uuid4()),
                                                        title='Gas Station',
                                                        description='Yesterday',
                                                        value=Decimal(10),
                                                        work_date=datetime.now().timestamp(),
                                                        receive_date=None,
                                                        received=False)


@contextmanager
def fake_uow():
    yield


def fake_authorized():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(request, *args, **kwargs):
            user = {'uid': str(uuid.uuid4())}
            return fn(request, user, *args, **kwargs)

        return wrapper

    return decorator


class BillingTestCase(unittest.TestCase):
    def setUp(self):
        app = Sanic()

        self._user_repository = Mock()
        self._add_billing = Mock()
        self._confirm_receive_billing = Mock()
        self._cancel_receive_billing = Mock()
        self._remove_billing = Mock()
        self._update_billing = Mock()

        init_billing(app=app,
                     uow=fake_uow,
                     authorized=fake_authorized,
                     user_repository=self._user_repository,
                     get_add_billing=Mock(return_value=self._add_billing),
                     get_confirm_receive_billing=Mock(return_value=self._confirm_receive_billing),
                     get_cancel_receive_billing=Mock(return_value=self._cancel_receive_billing),
                     get_remove_billing=Mock(return_value=self._remove_billing),
                     get_update_billing=Mock(return_value=self._update_billing))

        self._client = SanicTestClient(app, port=None)


class AddBillingTests(BillingTestCase):
    def test_should_add_billing_return_status_code_ok_when_use_case_is_valid(self):
        yesterday = datetime.now() + timedelta(days=1)

        data = {
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
            'title': 'Gas Station',
            'description': 'Yesterday',
            'value': 10,
            'work_date': yesterday.strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.post('/api/v1/billing', data=json.dumps(data))

        result = response.json['errors']

        expected = ['title should be inform']

        self.assertListEqual(expected, result)


class ConfirmReceiveBillingTests(BillingTestCase):
    def test_should_confirm_receive_billing_return_status_code_ok_when_use_case_is_valid(self):
        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/confirm-receive')

        self.assertEqual(200, response.status_code)

    def test_should_confirm_receive_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._confirm_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._confirm_receive_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/confirm-receive')

        self.assertEqual(400, response.status_code)

    def test_should_confirm_receive_billing_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._confirm_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._confirm_receive_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/confirm-receive')

        result = response.json['errors']

        expected = ['billing not exists']

        self.assertListEqual(expected, result)


class CancelReceiveBillingTests(BillingTestCase):
    def test_should_cancel_receive_billing_return_status_code_ok_when_use_case_is_valid(self):
        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/cancel-receive')

        self.assertEqual(200, response.status_code)

    def test_should_cancel_receive_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._cancel_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._cancel_receive_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/cancel-receive')

        self.assertEqual(400, response.status_code)

    def test_should_cancel_receive_billing_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._cancel_receive_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._cancel_receive_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.post(f'/api/v1/billing/{billing_uid}/cancel-receive')

        result = response.json['errors']

        expected = ['billing not exists']

        self.assertListEqual(expected, result)


class ListReceivedTests(BillingTestCase):
    def test_should_list_received_return_status_code_ok(self):
        _, response = self._client.get(f'/api/v1/billing/received')

        self.assertEqual(200, response.status_code)

    def test_should_list_received_return_a_list_of_billing_received(self):
        self._user_repository.list_billing_received.return_value = [FAKE_BILLING_LIST_QUERY_RESULT]

        _, response = self._client.get(f'/api/v1/billing/received')

        result = response.json['data']

        expected = [{'uid': FAKE_BILLING_LIST_QUERY_RESULT.uid,
                     'title': FAKE_BILLING_LIST_QUERY_RESULT.title,
                     'description': FAKE_BILLING_LIST_QUERY_RESULT.description,
                     'value': FAKE_BILLING_LIST_QUERY_RESULT.value,
                     'work_date': FAKE_BILLING_LIST_QUERY_RESULT.work_date,
                     'receive_date': FAKE_BILLING_LIST_QUERY_RESULT.receive_date,
                     'received': FAKE_BILLING_LIST_QUERY_RESULT.received}]

        self.assertEqual(expected, result)


class ListNotReceivedTests(BillingTestCase):
    def test_should_list_not_received_return_status_code_ok(self):
        _, response = self._client.get(f'/api/v1/billing/not-received')

        self.assertEqual(200, response.status_code)

    def test_should_list_not_received_return_a_list_of_billing_received(self):
        self._user_repository.list_billing_not_received.return_value = [FAKE_BILLING_LIST_QUERY_RESULT]

        _, response = self._client.get(f'/api/v1/billing/not-received')

        result = response.json['data']

        expected = [{'uid': FAKE_BILLING_LIST_QUERY_RESULT.uid,
                     'title': FAKE_BILLING_LIST_QUERY_RESULT.title,
                     'description': FAKE_BILLING_LIST_QUERY_RESULT.description,
                     'value': FAKE_BILLING_LIST_QUERY_RESULT.value,
                     'work_date': FAKE_BILLING_LIST_QUERY_RESULT.work_date,
                     'receive_date': FAKE_BILLING_LIST_QUERY_RESULT.receive_date,
                     'received': FAKE_BILLING_LIST_QUERY_RESULT.received}]

        self.assertEqual(expected, result)


class RemoveBillingTests(BillingTestCase):
    def test_should_remove_billing_return_status_code_ok_when_use_case_is_valid(self):
        billing_uid = str(uuid.uuid4())

        _, response = self._client.delete(f'/api/v1/billing/{billing_uid}')

        self.assertEqual(200, response.status_code)

    def test_should_remove_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._remove_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._remove_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.delete(f'/api/v1/billing/{billing_uid}')

        self.assertEqual(400, response.status_code)

    def test_should_remove_billing_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._remove_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._remove_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        _, response = self._client.delete(f'/api/v1/billing/{billing_uid}')

        result = response.json['errors']

        expected = ['billing not exists']

        self.assertListEqual(expected, result)


class UpdateBillingTests(BillingTestCase):
    def test_should_update_billing_return_status_code_ok_when_use_case_is_valid(self):
        billing_uid = str(uuid.uuid4())

        data = {
            'billing_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'yesterday',
            'value': 10,
            'work_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.put(f'/api/v1/billing/{billing_uid}', data=json.dumps(data))

        self.assertEqual(200, response.status_code)

    def test_should_update_billing_return_status_code_bad_request_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._update_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._update_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        data = {
            'billing_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'yesterday',
            'value': 10,
            'work_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.put(f'/api/v1/billing/{billing_uid}', data=json.dumps(data))

        self.assertEqual(400, response.status_code)

    def test_should_update_billing_return_errors_list_when_use_case_not_is_valid(self):
        is_valid = False
        billing_not_exists = Notification('billing', 'billing not exists')

        type(self._update_billing).is_valid = PropertyMock(return_value=is_valid)
        type(self._update_billing).notifications = PropertyMock(return_value=[billing_not_exists])

        billing_uid = str(uuid.uuid4())

        data = {
            'billing_uid': str(uuid.uuid4()),
            'title': 'Gas Station',
            'description': 'yesterday',
            'value': 10,
            'work_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        _, response = self._client.put(f'/api/v1/billing/{billing_uid}', data=json.dumps(data))

        result = response.json['errors']

        expected = ['billing not exists']

        self.assertListEqual(expected, result)
