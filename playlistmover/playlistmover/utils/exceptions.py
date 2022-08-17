from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class BadRequestException(Exception):
    """Bad Request data"""


class InternalServerException(Exception):
    """Server ran into errors processing request"""


def get_exception_response(exception: Exception):
    """
    Return the appropriate HTTP error response in case of exceptions
    """
    response = Response({"success": False, "error": str(exception)})
    if isinstance(exception, BadRequestException):
        response.status_code = HTTP_400_BAD_REQUEST
    else:
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    return response
