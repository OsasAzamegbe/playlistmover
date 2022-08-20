"""
    Test module for Playlist API
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "missing_params,query_params",
    (
        ("platform", {"code": "dummycode", "state": "dummystate"}),
        ("platform, code", {"state": "dummystate"}),
        ("platform, code, state", {}),
    ),
)
def test_get_playlist_without_platform(api_client, missing_params, query_params):
    """Test error response when there are query parameters missing"""
    url = reverse("playlists")
    expected_response = {
        "success": False,
        "error": "`{}` in request is invalid.".format(missing_params),
    }

    response = api_client.get(url, data=query_params, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response


def test_get_playlist_with_invalid_platform(api_client):
    """Test error response when unsupported platform is given"""
    platform = "NonesensePlatform"
    query_params = {"platform": platform, "code": "DummyCode", "state": "DummyState"}
    url = reverse("playlists")
    expected_response = {
        "success": False,
        "error": "`{}` not supported.".format(platform),
    }

    response = api_client.get(url, data=query_params, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "code,state",
    (
        ("DummyCode", "Dummystate"),
        ("DummyCode", "123456789abcdefg"),
    ),
)
def test_get_playlist_with_invalid_auth(api_client, code, state):
    """Test error response when auth is invalid"""
    query_params = {"platform": "SPOTIFY", "code": code, "state": state}
    url = reverse("playlists")
    expected_response = {
        "success": False,
        "error": "User is unauthorized.",
    }

    response = api_client.get(url, data=query_params, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == expected_response
