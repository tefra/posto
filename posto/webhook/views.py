from typing import Any
from typing import Dict

from flask import Blueprint
from flask import request

from posto.utils import validators
from posto.webhook import auth

blueprint = Blueprint("webhook", __name__)


@blueprint.route("/", methods=["POST"])
@validators.require_json()
@auth.authorize_source()
def post(*args: Any, source: str, **kwargs: Any) -> Dict:
    request.json  # We will store this...

    return {
        "code": 200,
        "status": "Roger",
        "description": "Event notification received",
    }
