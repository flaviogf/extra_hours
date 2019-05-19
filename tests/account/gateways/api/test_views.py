import unittest

from extra_hours.account.gateways.api import create_app


class AccountTests(unittest.TestCase):
    def setUp(self):
        config = 'extra_hours.account.gateways.api.config.TestingConfig'

        app = create_app(config=config)

        self._client = app.test_client()

    def test_should_create_billing_return_status_code_ok(self):
        json = {
            'email': 'captain@marvel.com.br',
            'password': 'test123567'
        }

        response = self._client.post('/api/v1/account', json=json)

        self.assertEqual(201, response.status_code)
