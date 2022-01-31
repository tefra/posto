import abc
import json
import logging
from typing import Any
from typing import Dict

from elasticsearch import Elasticsearch


class BaseAdapter(abc.ABC):
    """Abstract analytics adapter class."""

    __slots__ = ()

    @abc.abstractmethod
    def emit(self, index: str, document: Dict):
        """"""


class LogAdapter(BaseAdapter):
    """Log adapter to emit events to the StdOut."""

    __slots__ = "engine"

    def __init__(self, **kwargs: Any):
        name = kwargs.pop("name", "analytics-logger")
        self.engine = logging.getLogger(name)

    def emit(self, index: str, document: Dict):
        self.engine.info(json.dumps({"index": index, "document": document}))


class ElasticSearchAdapter(BaseAdapter):
    """Elastic search adapter to emit events to a specific index."""

    __slots__ = "engine"

    def __init__(self, **kwargs: Any):
        self.engine = Elasticsearch(**kwargs)

    def emit(self, index: str, document: Dict):
        self.engine.index(index=index, document=document)
