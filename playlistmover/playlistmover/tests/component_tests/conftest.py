from unittest import mock
import pytest
from rest_framework.test import APIClient
from rest_framework import status


ACCESS_TOKEN = "this_is_dummy_access_token"
REFRESH_TOKEN = "this_is_dummy_refresh_token"
CODE = "this_is_dummy_code"
STATE = "123456789abcdefg"


@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient()


def mock_requests_get(url, params, headers, *args, **kwargs):
    """Mock GET response"""
    mocked_response = mock.Mock()
    mocked_response.status_code.return_value = status.HTTP_200_OK
    mocked_response.json.return_value = {}
    return mocked_response


def mock_requests_post(url, data, headers, *args, **kwargs):
    """Mock POST response"""
    mocked_response = mock.Mock()
    mocked_response.status_code.return_value = status.HTTP_200_OK
    mocked_response.json.return_value = {
        "access_token": ACCESS_TOKEN,
        "refresh_token": REFRESH_TOKEN,
    }
    return mocked_response


@pytest.fixture
def mock_requests_module():
    """Mock request module"""
    with mock.patch("playlistmover.playlistmover.utils.clients.requests") as mock_requests:
        mock_requests.get.side_effect = mock_requests_get
        mock_requests.post.side_effect = mock_requests_post
        yield mock_requests
