import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from unittest import mock
from unittest import TestCase

from posto import AnalyticsClient
from posto.analytics.adapters import BaseAdapter
from posto.webhook.processor import EventProcessor
from posto.webhook.processor import GithubMapper
from posto.webhook.processor import GitlabMapper
from posto.webhook.processor import Record


class DummyAnalytics(AnalyticsClient):
    def __init__(self):
        self.data = []

    def emit(self, index: str, document: Dict):
        self.data.append((index, document))


class EventProcessorTests(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.ep = EventProcessor("tests", DummyAnalytics())

    @mock.patch.object(GitlabMapper, "map")
    def test_ingest(self, mock_map):
        record = Record(
            timestamp="foo",
            user="me",
            event="test_ingest",
            source="tests",
            repo="this/one",
        )
        mock_map.return_value = record

        self.ep.ingest("gitlab", {}, {})

        expected = [("tests", record._asdict())]
        self.assertEqual(expected, self.ep.analytics.data)


class GithubMapperTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.mapper = GithubMapper()

    @mock.patch("posto.webhook.processor.get_now")
    def test_map(self, mock_now):

        mock_now.return_value = datetime(2020, 1, 6, 18, 15, 30)
        headers = {"X-Github-Event": "testing"}
        event = Path(__file__).parent.joinpath("samples/github_new_issue.json")

        actual = self.mapper.map(headers, json.load(event.open()))
        expected = Record(
            user="tefra",
            repo="tefra/posto",
            event="testing_created",
            source="github",
            timestamp="2020-01-06T18:15:30",
        )
        self.assertEqual(expected, actual)


class GitlabMapperTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.mapper = GitlabMapper()

    @mock.patch("posto.webhook.processor.get_now")
    def test_map(self, mock_now):

        mock_now.return_value = datetime(2020, 1, 6, 18, 15, 30)
        event = Path(__file__).parent.joinpath("samples/gitlab_new_issue.json")

        actual = self.mapper.map({}, json.load(event.open()))
        expected = Record(
            user="tefra",
            repo="tefra/posto",
            event="issue_opened",
            source="gitlab",
            timestamp="2020-01-06T18:15:30",
        )
        self.assertEqual(expected, actual)
