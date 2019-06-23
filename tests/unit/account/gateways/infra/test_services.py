import unittest

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.value_objects import Email, Password


class JwtTokenServiceTests(unittest.TestCase):
    def setUp(self):
        self._token_service = JwtTokenService('secret')

    def test_should_encode_return_jwt_token(self):
        email = Email('naruto@uzumaki.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        token = self._token_service.encode(naruto)

        self.assertIsInstance(token, str)

    def test_should_decode_return_dict_when_token_is_valid(self):
        email = Email('naruto@uzumaki.com')
        password = Password('sasuke123')
        naruto = User(email, password)

        token = self._token_service.encode(naruto)

        user = self._token_service.decode(token)

        self.assertIsInstance(user, dict)

    def test_should_decode_return_none_when_token_not_is_valid(self):
        user = self._token_service.decode('')

        self.assertIsNone(user)
