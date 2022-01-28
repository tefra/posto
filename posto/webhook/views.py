from typing import Any
from typing import Dict

from flask import Blueprint

from posto.utils import validators
from posto.webhook import auth

blueprint = Blueprint("webhook", __name__)


@blueprint.route("/", methods=["POST"])
@validators.json_required()
@auth.parse_header_token()
def home(*args: Any, source: str, **kwargs: Any) -> Dict:
    return {"status": "received"}
