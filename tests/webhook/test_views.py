import hmac
from unittest import TestCase

import pytest

from tests.utils import ViewTestCase


class ViewTests(ViewTestCase):
    def test_home(self):
        expected = {"code": 200, "description": "I am posto: 1.0.0", "status": "OK"}
        response = self.client.get("/")
        self.assertEqual(expected, response.json)

    def test_errors(self):
        expected = {
            "code": 404,
            "description": "The requested URL was not found on the server. If you entered "
            "the URL manually please check your spelling and try again.",
            "status": "Not Found",
        }
        response = self.client.get("/unknown/")
        self.assertEqual(expected, response.json)
