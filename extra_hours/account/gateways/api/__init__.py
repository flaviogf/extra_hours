from flask import Flask

from extra_hours.account.gateways.api.views import create_account

DEFAULT_CONFIG = 'extra_hours.account.gateways.api.config.Config'


def create_app(config=DEFAULT_CONFIG):
    app = Flask(__name__)

    app.config.from_object(config)

    account = create_account(app)

    app.register_blueprint(account)

    return app
