import jwt
from jwt import DecodeError


class JwtTokenService:
    def __init__(self, secret_key):
        self._secret_key = secret_key

    def encode(self, user):
        token = jwt.encode({'uid': user.uid, 'email': user.email}, key=self._secret_key, algorithm='HS256')

        token = token.decode('utf-8')

        return token

    def decode(self, token):
        try:
            return jwt.decode(token, self._secret_key, algorithms=['HS256'])
        except DecodeError:
            return
