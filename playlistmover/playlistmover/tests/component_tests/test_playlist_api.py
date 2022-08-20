"""
    Test module for Playlist API
"""
import pytest
from django.urls import reverse
from rest_framework import status


def test_get_playlist_without_platform(api_client):
    """Test error response when platform query parameter is missing"""
    url = reverse("playlists")
    query_params = {"code": "dummycode", "state": "dummystate"}
    expected_response = {"success": False, "error": "`platform` in request is invalid."}

    response = api_client.get(url, data=query_params, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response
