import unittest
import uuid
from unittest.mock import Mock, PropertyMock

import jwt
from flask import Flask, g

from extra_hours.account.gateways.api.middlewares import init_account_middleware


class AccountMiddlewareTests(unittest.TestCase):
    def setUp(self):
        self._app = Flask(__name__)

        self._secret = 'test'

        self._config = Mock()

        type(self._config).SECRET_KEY = PropertyMock(return_value=self._secret)

    def test_should_user_is_available_in_flask_global_context_when_token_is_informed(self):
        self._create_fake_route()

        init_account_middleware(self._app, self._config)

        payload = {
            'uid': str(uuid.uuid4()),
            'email': 'perter@marvel.com'
        }

        token = jwt.encode(payload, self._secret).decode('utf-8')

        with self._app.test_request_context('/', headers={'Authorization': token}):
            self._app.preprocess_request()

            self.assertDictEqual(payload, g.user)

    def test_should_user_not_is_available_in_flask_global_context_when_token_not_is_informed(self):
        self._create_fake_route()

        init_account_middleware(self._app, self._config)

        with self._app.test_request_context('/'):
            self._app.preprocess_request()

            self.assertDictEqual({}, g.user)

    def _create_fake_route(self):
        @self._app.route('/')
        def index():
            return 'OK'
