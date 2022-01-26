import os
from typing import Type


class Config:
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv("SECRET_KEY", default="A very terrible secret key.")


class DevelopmentConfig(Config):
    FLASK_ENV = "dev"
    DEBUG = True


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
