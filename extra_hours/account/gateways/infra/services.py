import uuid

import jwt
import requests

from extra_hours.account.entities import User


class FirebaseUserService:
    def __init__(self, config):
        self._config = config

    def sign_with_email_and_password(self, email, password):
        url_api = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}'

        data = {
            'email': email,
            'password': password,
        }

        response = requests.post(url_api.format('AIzaSyBSutdXuiHNq9JqSkN8Zqx9EpAhcQY7g9M'), data=data)

        if response.status_code != 200:
            return None, None

        json = response.json()

        payload = {
            'uid': json['localId'],
            'email': email,
        }

        token = jwt.encode(payload, self._config.SECRET_KEY).decode('utf-8')

        user = User(email=email,
                    password=password,
                    uid=uuid.UUID(json['localId']))

        return user, token
