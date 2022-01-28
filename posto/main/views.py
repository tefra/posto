import json
from typing import Dict

from flask import Blueprint
from flask import Response
from werkzeug.exceptions import HTTPException

from posto import __version__


blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index() -> Dict:
    return {
        "code": 200,
        "status": "OK",
        "description": f"I am posto: {__version__}",
    }


@blueprint.app_errorhandler(HTTPException)
def handle_exception(e: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors."""

    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "status": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
