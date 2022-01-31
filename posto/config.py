import os
from typing import Type


class Config:
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv("SECRET_KEY", default="A very terrible secret key.")

    # You might want to update these in production
    GITLAB_SECRET = "supersecret"
    GITHUB_SECRET = "supersecret"

    # See class constructor arguments
    ANALYTICS = {
        "adapter": "posto.analytics.adapters.LogAdapter",
        "name": "analytics-logger",
    }

    LOGGING = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }


class DevelopmentConfig(Config):
    FLASK_ENV = "dev"
    DEBUG = True

    # https://elasticsearch-py.readthedocs.io/en/v7.16.3/api.html#elasticsearch
    # All params except the adapter will pass as keyword arguments to the client
    ANALYTICS = {
        "adapter": "posto.analytics.adapters.ElasticSearchAdapter",
        "hosts": "http://localhost:9200",
        # http_auth = (“username”, “password”)
        # api_key=(“api_key_id”, “api_key_secret”)
    }


class TestingConfig(Config):
    FLASK_ENV = "dev"
    TESTING = True


class ProductionConfig(Config):
    FLASK_ENV = "production"


def get_config() -> Type[Config]:
    """Return the correct config class based on the FLASK_ENV variable."""

    env = os.environ.get("FLASK_ENV")
    if env in ("prod", "production"):
        return ProductionConfig

    if env in ("test", "testing"):
        return TestingConfig

    return DevelopmentConfig
