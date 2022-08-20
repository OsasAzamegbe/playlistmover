from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestPlaylistApiView(APITestCase):
    """
    Test module for Playlist API
    """

    def test_get_playlist_without_platform(self):
        """Test error response when platform query parameter is missing"""
        url = reverse("playlists")
        query_params = {"code": "dummycode", "state": "dummystate"}
        expected_response = {"success": False, "error": "`platform` in request is invalid."}

        response = self.client.get(url, data=query_params, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), expected_response)
