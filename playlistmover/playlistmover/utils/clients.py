from typing import Any, Dict, List, Optional

import requests
from playlistmover.playlistmover.models import Playlist, Song
from playlistmover.playlistmover.serializers import PlaylistSerializer


class Client:
    """
    HTTP client base-class
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_get_request(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Send HTTP GET request to API endpoint
        """
        return requests.get(f"{self.base_url}/{endpoint}", params=params)

    def send_post_request(
        self, endpoint: str, request_data: Optional[Dict[str, Any]]
    ) -> requests.Response:
        """
        Send HTTP POST request to API endpoint
        """
        return requests.post(f"{self.base_url}/{endpoint}", data=request_data)


class Spotify:
    """
    Spotify Interface
    """

    def __init__(self):
        self.client = Client("www.spotify.com/api/")  # dummy endpoint

    def get_playlists(self, request) -> List[Playlist]:
        """
        Get list of playlists from Spotify account
        """
        songs = [Song("Last last", "Burna Boy"), Song("Jailer", "Asa")]
        playlist = Playlist("naija", songs)
        playlist2 = Playlist("Afro beats", songs)
        return [playlist, playlist2]

    def create_playlists(self, request, playlists: PlaylistSerializer) -> List[Dict[str, Any]]:
        """
        Create list of playlists on Spotify account
        """
        print(playlists.create(playlists.validated_data))
        return playlists.validated_data
