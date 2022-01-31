from typing import Any
from typing import Dict

from flask import Blueprint
from flask import request

from posto import analytics
from posto.utils import validators
from posto.webhook import auth
from posto.webhook.processor import EventProcessor

blueprint = Blueprint("webhook", __name__)


@blueprint.route("/", methods=["POST"])
@validators.require_json()
@auth.authorize_source()
def post(*args: Any, source: str, **kwargs: Any) -> Dict:
    processor = EventProcessor("webhooks", analytics)
    processor.ingest(source, dict(request.headers), request.json)

    return {
        "code": 200,
        "status": "Roger",
        "description": "Event notification received",
    }
