import functools
from typing import Any, Dict, List

from playlistmover.playlistmover.logic.exceptions import (
    BadRequestException,
    get_exception_response,
)


def is_valid_request(request_name: str, request) -> str:
    """Validates the request passed in for the given request_name"""
    query_params: Dict[str, Any] = request.query_params
    data: Dict[str, Any] = request.data
    invalid_fields: List[str] = []

    def check_field(object: Dict[str, Any], field: str):
        if field not in object:
            invalid_fields.append(field)

    def check_fields(object: Dict[str, Any], *fields: tuple[str]):
        for field in fields:
            check_field(object, field)

    if request_name == "getPlaylists":
        check_fields(query_params, "platform", "code", "state", "redirect_uri")
    elif request_name == "postPlaylists":
        check_fields(data, "playlists", "context")
        check_field(data.get("context", {}), "platform")
    elif request_name == "getAuth":
        check_fields(query_params, "platform", "redirect_uri")

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
