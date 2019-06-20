import jwt
from jwt import DecodeError


class JwtTokenService:
    def __init__(self, secret):
        self._secret = secret

    def encode(self, user):
        user_dict = {
            'uid': user.uid,
            'email': user.email
        }

        return jwt.encode(user_dict, key=self._secret, algorithm='HS256')

    def decode(self, token):
        try:
            return jwt.decode(token, self._secret, algorithms=['HS256'])
        except DecodeError:
            return None
