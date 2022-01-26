__version__ = "1.0.0"

from flask import Flask
from posto.config import get_config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    from posto import webhook

    app.register_blueprint(webhook.blueprint, url_prefix="/webhook")
    app.add_url_rule("/", endpoint="index")

    return app
