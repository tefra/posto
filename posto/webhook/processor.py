import abc
import datetime
from typing import Dict
from typing import NamedTuple

from posto import AnalyticsClient


def get_now() -> datetime.datetime:
    return datetime.datetime.now()


class Record(NamedTuple):
    user: str
    repo: str
    event: str
    source: str
    timestamp: str


class Mapper(abc.ABC):
    """Abstract mapper class."""

    @classmethod
    @abc.abstractmethod
    def map(cls, headers: Dict, event: Dict) -> Record:
        """Use the event body and hears to create a record for storage."""


class EventProcessor:
    """
    Event notification orchestrator.

    The processor must first ingest the message into a record with a
    fixed structure and then dispatch it to storage. All exceptions are
    propagated!!!
    """

    __slots__ = "index", "mappers", "analytics"

    def __init__(self, index: str, analytics: AnalyticsClient):
        """Initialize instance with an empty mappers list and soon the storage
        client."""
        self.index = index
        self.analytics = analytics
        self.mappers = {"github": GithubMapper(), "gitlab": GitlabMapper()}

    def ingest(self, source: str, headers: Dict, event: Dict):
        """Create a record form the headers and body based on the source and
        save it."""
        record = self.mappers[source].map(headers, event)
        self.emit(record)

    def emit(self, record: Record):
        """Emit the record to the analytics client to the specified index."""
        self.analytics.emit(index=self.index, document=record._asdict())


class GithubMapper(Mapper):
    @classmethod
    def map(cls, headers: Dict, event: Dict) -> Record:
        gh_event = headers["X-Github-Event"]
        gh_action = event["action"]

        return Record(
            timestamp=get_now().isoformat(),
            user=event["sender"]["login"],
            event=f"{gh_event}_{gh_action}",
            source="github",
            repo=event["repository"]["full_name"],
        )


class GitlabMapper(Mapper):
    @classmethod
    def map(self, headers: Dict, event: Dict) -> Record:
        gl_event = event["event_type"]
        gl_action = event["object_attributes"]["state"]

        return Record(
            timestamp=get_now().isoformat(),
            user=event["user"]["username"],
            event=f"{gl_event}_{gl_action}",
            source="gitlab",
            repo=event["repository"]["homepage"].replace("https://gitlab.com/", ""),
        )
