import unittest

from flask import Flask

from extra_hours.shared.gateways.api.responses import ok, bad_request, no_authorized, created


class ResponseTestCase(unittest.TestCase):
    def setUp(self):
        self._app = Flask(__name__)


class OkTests(ResponseTestCase):
    def test_should_ok_return_response_with_data(self):
        with self._app.app_context():
            response, _ = ok('user authenticated')

            expected_response = {'data': 'user authenticated', 'errors': []}

            self.assertDictEqual(expected_response, response.json)

    def test_should_ok_return_status_code_200(self):
        with self._app.app_context():
            _, status_code = ok('user authenticated')

            expected_status_code = 200

            self.assertEqual(expected_status_code, status_code)


class CreatedTests(ResponseTestCase):
    def test_should_create_return_response_with_data(self):
        with self._app.app_context():
            response, _ = created('user created')

            expected_response = {'data': 'user created', 'errors': []}

            self.assertDictEqual(expected_response, response.json)

    def test_should_create_return_status_code_201(self):
        with self._app.app_context():
            _, status_code = created('user created')

            expected_status_code = 201

            self.assertEqual(expected_status_code, status_code)


class BadRequestTests(ResponseTestCase):
    def test_should_bad_request_return_response_with_errors(self):
        with self._app.app_context():
            user_not_exists = 'user not exists'

            response, _ = bad_request(errors=[user_not_exists])

            expected_response = {'data': None, 'errors': [user_not_exists]}

            self.assertDictEqual(expected_response, response.json)

    def test_should_bad_request_return_status_code_400(self):
        with self._app.app_context():
            user_not_exists = 'user not exists'

            _, status_code = bad_request(errors=[user_not_exists])

            expected_status_code = 400

            self.assertEqual(expected_status_code, status_code)


class NoAuthorizedTests(ResponseTestCase):
    def test_should_not_authorized_return_response_with_errors(self):
        with self._app.app_context():
            user_not_authenticated = 'user not authenticated'

            response, _ = no_authorized(errors=[user_not_authenticated])

            expected_response = {'data': None, 'errors': [user_not_authenticated]}

            self.assertDictEqual(expected_response, response.json)

    def test_should_no_authorized_return_status_code_401(self):
        with self._app.app_context():
            user_not_authenticated = 'user not authenticated'

            _, status_code = no_authorized(errors=[user_not_authenticated])

            expected_status_code = 401

            self.assertEqual(expected_status_code, status_code)
