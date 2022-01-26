from typing import Dict

from flask import Blueprint


blueprint = Blueprint("webhook", __name__)


@blueprint.route("/", methods=["POST"])
def home() -> Dict:

    return {"status": "received"}
