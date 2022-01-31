import functools
import hmac
from typing import Any
from typing import Callable
from typing import Optional

from flask import abort
from flask import current_app
from flask import request
from werkzeug.exceptions import ServiceUnavailable


def authorize_source() -> Callable:
    """Detect the source from the headers and authenticate by the config
    secret."""

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            source = next(
                (
                    authorize_func()
                    for name, authorize_func in __PARSERS__.items()
                    if name in request.headers
                ),
                None,
            )

            if source is None:
                abort(401)
            return fn(*args, source=source, **kwargs)

        return wrapper

    return decorator


def authorize_gitlab() -> Optional[str]:
    """
    Check gitlab header token is correct and return the source name.

    The token is raw because gitlab only allows for ssl endpoints.
    """
    source = "gitlab"
    if get_secret(source) == request.headers["X-Gitlab-Token"]:
        return source

    return None


def authorize_github() -> Optional[str]:
    """
    Verify github signature matches our secret with the payload and return the
    source name.

    Github uses HMAC signature verification, encode the payload with the
    secret
    """

    source = "github"
    secret = get_secret(source)
    signature = request.headers["X-Hub-Signature"]

    signature_prefix = "sha1="
    if not signature.startswith(signature_prefix):
        return None

    hmac_ = hmac.new(secret.encode("UTF-8"), msg=request.data, digestmod="sha1")
    calculated_sig = signature_prefix + hmac_.hexdigest()
    if not hmac.compare_digest(signature, calculated_sig):
        return None

    return source


def get_secret(source: str) -> str:
    """Get the secret key from config by the source or raise an exception."""
    secret = current_app.config.get(f"{source.upper()}_SECRET", None)

    if secret is None:
        raise ServiceUnavailable(f"Missing {source} secret")

    return secret


__PARSERS__ = {
    "X-Gitlab-Token": authorize_gitlab,
    "X-Hub-Signature": authorize_github,
}
