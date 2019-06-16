import unittest

from extra_hours.account.gateways.infra.services import JwtTokenService


class JwtTokenServiceTests(unittest.TestCase):
    def test_should_encode(self):
        jwt_token_service = JwtTokenService()

        jwt_token_service.encode(None)

        self.assertTrue(True)

    def test_should_decode(self):
        jwt_token_service = JwtTokenService()

        jwt_token_service.decode(None)

        self.assertTrue(True)
