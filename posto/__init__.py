__version__ = "1.0.0"

from logging.config import dictConfig

from flask import Flask

from posto.analytics import AnalyticsClient
from posto.config import get_config

analytics = AnalyticsClient()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    if isinstance(app.config.get("LOGGING"), dict):
        dictConfig(app.config["LOGGING"])

    analytics.init_app(app)

    from posto import webhook
    from posto import main

    app.register_blueprint(main.blueprint)
    app.register_blueprint(webhook.blueprint, url_prefix="/webhook")

    return app
