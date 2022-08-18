import functools
from typing import Any, Dict, List

from playlistmover.playlistmover.utils.exceptions import (
    BadRequestException,
    get_exception_response,
)


def is_valid_request(request_name: str, request) -> str:
    """Validates the request passed in for the given request_name"""
    query_params: Dict[str, Any] = request.query_params
    data: Dict[str, Any] = request.data
    invalid_fields: List[str] = []

    def check_field(field: str, object: Dict[str, Any]):
        if field not in object:
            invalid_fields.append(field)

    if request_name == "getPlaylists":
        for field in ("platform", "code", "state"):
            check_field(field, query_params)
    elif request_name == "postPlaylists":
        for field in ("playlists", "context"):
            check_field(field, data)
        check_field("platform", data.get("context", {}))
    elif request_name == "getAuth":
        check_field("platform", query_params)

    return ", ".join(invalid_fields)


def request_validator(request_name: str):
    """Wrapper around view handlers to validate incoming requests"""

    def request_validator_wrapper(view_handler):
        @functools.wraps(view_handler)
        def wrapper(self, request, *args, **kwargs):
            invalid_fields: str = is_valid_request(request_name, request)
            if invalid_fields:
                return get_exception_response(
                    BadRequestException(
                        "`{}` in request is invalid.".format(invalid_fields)
                    )
                )
            return view_handler(self, request, *args, **kwargs)

        return wrapper

    return request_validator_wrapper
