import hmac
from unittest import mock
from unittest import TestCase

import pytest

from posto.webhook.processor import EventProcessor
from tests.utils import ViewTestCase


class PostTests(ViewTestCase):
    def test_requires_post(self):
        expected = {
            "code": 405,
            "status": "Method Not Allowed",
            "description": "The method is not allowed for the requested URL.",
        }
        response = self.client.get("/webhook/")
        self.assertEqual(expected, response.json)

    def test_requires_json_content_type(self):
        response = self.client.post(
            "/webhook/", content_type="application/xml", data="irrelevant"
        )
        expected = {
            "code": 406,
            "status": "Not Acceptable",
            "description": "The resource identified by the request is only capable of "
            "generating response entities which have content "
            "characteristics not acceptable according to the accept "
            "headers sent in the request.",
        }
        self.assertEqual(expected, response.json)

    @mock.patch.object(EventProcessor, "ingest")
    def test_authorize_source_gitlab(self, mock_ingest):
        secret = self.client.application.config["GITLAB_SECRET"]
        response = self.client.post(
            "/webhook/",
            content_type="application/json",
            data="{}",
            headers={"X-Gitlab-Token": secret},
        )

        expected = {
            "code": 200,
            "description": "Event notification received",
            "status": "Roger",
        }
        self.assertEqual(expected, response.json)
        mock_ingest.assert_called_once_with(
            "gitlab", dict(response.request.headers), {}
        )

    @mock.patch.object(EventProcessor, "ingest")
    def test_authorize_source_github(self, mock_ingest):
        secret = self.client.application.config["GITHUB_SECRET"]
        data = "{}"
        hmac_ = hmac.new(secret.encode("UTF-8"), msg=data.encode(), digestmod="sha1")
        signature = f"sha1={hmac_.hexdigest()}"

        response = self.client.post(
            "/webhook/",
            content_type="application/json",
            data=data,
            headers={"X-Hub-Signature": signature},
        )

        expected = {
            "code": 200,
            "description": "Event notification received",
            "status": "Roger",
        }
        self.assertEqual(expected, response.json)
        mock_ingest.assert_called_once_with(
            "github", dict(response.request.headers), {}
        )

    def test_requires_valid_json(self):
        secret = self.client.application.config["GITLAB_SECRET"]
        response = self.client.post(
            "/webhook/",
            content_type="application/json",
            data="broken",
            headers={"X-Gitlab-Token": secret},
        )
        expected = {
            "code": 400,
            "description": "The browser (or proxy) sent a request that this server could "
            "not understand.",
            "status": "Bad Request",
        }
        self.assertEqual(expected, response.json)
