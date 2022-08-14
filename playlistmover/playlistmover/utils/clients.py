from typing import Any, Dict, List, Optional

import requests
from playlistmover.playlistmover.clients_enums import ClientEnum
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
        return requests.get("{}{}".format(self.base_url, endpoint), params=params)

    def send_post_request(
        self, endpoint: str, request_data: Optional[Dict[str, Any]]
    ) -> requests.Response:
        """
        Send HTTP POST request to API endpoint
        """
        return requests.post("{}{}".format(self.base_url, endpoint), data=request_data)

    @staticmethod
    def get_client(client_enum: ClientEnum):
        """
        Factory static method for getting a client based on the passed Enum
        """
        if client_enum == ClientEnum.SPOTIFY:
            return SpotifyClient()


class SpotifyClient(Client):
    """
    Spotify Client Interface
    """

    def __init__(self):
        super().__init__("https://api.spotify.com/v1/")

    def get_playlists(self, context: Dict[str, str]) -> List[Playlist]:
        """
        Get list of playlists from Spotify account
        """
        try:
            response = self.send_get_request("me")
            print(response.json())
            user_id = response.json()["uri"].split(":")[-1]
            endpoint = "users/{}/playlists".format(user_id)
            response = self.send_get_request(endpoint)
            print(response)
        except:
            """Dummy for now"""
            pass
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
