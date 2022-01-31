import importlib
from typing import Dict
from typing import Optional
from typing import Type

from flask import Flask

from posto.analytics.adapters import BaseAdapter


class AnalyticsConfigError(Exception):
    pass


class AnalyticsClient:
    __slots__ = "adapter"

    def __init__(self):
        self.adapter: Optional[BaseAdapter] = None

    def init_app(self, app: Flask):
        config = app.config.get("ANALYTICS")
        if config is None:
            raise AnalyticsConfigError("Missing config `ANALYTICS`")

        adapter_qualified_name = config.pop("adapter", "")
        if not adapter_qualified_name:
            raise AnalyticsConfigError("Missing adapter class")

        adapter_class = self.discover_adapter(adapter_qualified_name)
        self.adapter = adapter_class(**config)

    def emit(self, index: str, document: Dict):
        if self.adapter is None:
            raise AnalyticsConfigError("Adapter is not initialized")

        self.adapter.emit(index, document)

    @classmethod
    def discover_adapter(cls, qualified_name: str) -> Type:
        try:
            module_path, class_name = qualified_name.rsplit(".", 1)
        except ValueError as err:
            raise ImportError(
                "%s doesn't look like a module path" % qualified_name
            ) from err

        module = importlib.import_module(module_path)
        return getattr(module, class_name)
