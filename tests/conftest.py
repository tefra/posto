import os
import tempfile

import pytest

from posto import create_app


@pytest.fixture(scope="class", autouse=True)
def client():
    os.environ.setdefault("FLASK_ENV", "test")
    app = create_app()

    with app.test_client() as client:
        yield client
