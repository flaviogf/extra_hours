import jwt
from flask import request, g
from jwt import DecodeError


def init_account_middleware(app, config):
    @app.before_request
    def account_middleware():
        g.user = {}

        token = request.headers.get('Authorization')

        if not token:
            return

        try:
            g.user = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        except DecodeError:
            pass
