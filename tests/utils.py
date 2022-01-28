import os
from unittest import TestCase

from posto import create_app


class ViewTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ.setdefault("FLASK_ENV", "test")
        os.environ.setdefault("FLASK_DEBUG", "1")
        app = create_app()
        self.client = app.test_client()
