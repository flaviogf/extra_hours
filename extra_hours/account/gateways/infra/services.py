import jwt


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
        return jwt.decode(token, self._secret, algorithms=['HS256'])
