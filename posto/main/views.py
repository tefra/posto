import json
import logging
from typing import Dict
from typing import Tuple

from flask import Blueprint
from flask import current_app
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


@blueprint.app_errorhandler(Exception)
def handle_unhandled_exception(e: Exception) -> Tuple[Dict, int]:
    """Return JSON instead of HTML for HTTP errors."""

    # start with the correct headers and status code from the error

    logging.error(e)

    return {
        "code": 500,
        "status": "Internal Server Error",
        "description": repr(e)
        if current_app.debug
        else "Something's broken, something's broken, it's your fault!",
    }, 500
