import unittest

import jwt

from extra_hours.account.entities import User
from extra_hours.account.gateways.infra.services import JwtTokenService
from extra_hours.account.value_objects import Email, Password


class JwtTokenServiceTests(unittest.TestCase):
    def setUp(self):
        self._naruto = User(email=Email('naruto@uzumaki.com'), password=Password('test123'))

        self._secret = 'secret'

        self._jwt_token_service = JwtTokenService(self._secret)

    def test_should_encode_return_jwt_token_with_user_uid(self):
        token = self._jwt_token_service.encode(self._naruto)

        user = jwt.decode(token, self._secret, algorithms=['HS256'])

        self.assertEqual(self._naruto.uid, user.get('uid'))

    def test_should_encode_return_jwt_token_with_user_email(self):
        token = self._jwt_token_service.encode(self._naruto)

        user = jwt.decode(token, self._secret, algorithms=['HS256'])

        self.assertEqual(self._naruto.email, user.get('email'))

    def test_should_decode_return_user_dict_with_uid(self):
        jwt_token_service = JwtTokenService(self._secret)

        expected = {
            'uid': self._naruto.uid,
            'email': self._naruto.email
        }

        token = jwt.encode(expected, self._secret, algorithm='HS256')

        result = jwt_token_service.decode(token)

        self.assertDictEqual(expected, result)

    def test_should_decode_return_none_when_token_not_is_valid(self):
        jwt_token_service = JwtTokenService(self._secret)

        token = jwt_token_service.decode('xpto')

        self.assertIsNone(token)
