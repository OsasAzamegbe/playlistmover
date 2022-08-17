import os
import requests
from requests.models import PreparedRequest
from typing import Any, Dict, List, Optional

from playlistmover.playlistmover.clients_enums import ClientEnum
from playlistmover.playlistmover.models import Playlist, Song
from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.utils.utils import encode_string_base64


class Client:
    """
    HTTP client base-class
    """

    def __init__(self, base_url: str = ""):
        self.base_url = base_url

    def send_get_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Send HTTP GET request to API endpoint
        """
        return requests.get("{}{}".format(self.base_url, endpoint), params=params, headers=headers)

    def send_post_request(
        self,
        endpoint: str,
        request_data: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Send HTTP POST request to API endpoint
        """
        return requests.post(
            "{}{}".format(self.base_url, endpoint), data=request_data, headers=headers
        )

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
        self.state = "123456789abcdefg"
        self.redirect_uri = "http://127.0.0.1:8000/api/playlists?platform=SPOTIFY"
        self.access_token = self.refresh_token = ""
        self.headers = {}
        super().__init__()

    @staticmethod
    def _get_id_from_uri(uri: str) -> str:
        """
        Parse the `id` from a spotify uri of the form spotify:type:id
        """
        return uri.split(":")[-1]

    def get_playlists(self, context: Dict[str, str]) -> List[Playlist]:
        """
        Get list of playlists from Spotify account
        """
        self._setup_auth_tokens(context)
        user_id = self._get_user_id()
        endpoint = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        params = {"limit": 50}
        response = self.send_get_request(endpoint, params=params, headers=self.headers)
        response_json = response.json()
        playlists: List[Playlist] = [
            self._get_playlist(playlist) for playlist in response_json["items"]
        ]
        return playlists

    def create_playlists(self, request, playlists: PlaylistSerializer) -> List[Dict[str, Any]]:
        """
        Create list of playlists on Spotify account
        """
        print(playlists.create(playlists.validated_data))
        return playlists.validated_data

    def get_authorization_url(self) -> str:
        """
        Initialize authentication of user through Spotify
        """
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        scope = "playlist-modify-private playlist-read-private"

        req_builder = PreparedRequest()
        url = "https://accounts.spotify.com/authorize"
        params = {
            "response_type": "code",
            "client_id": client_id,
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
        }
        req_builder.prepare_url(url, params)
        return req_builder.url

    def _setup_auth_tokens(self, context: Dict[str, str]):
        """
        get authentication options after setting up initial authentication with Spotify
        """
        code = context["code"]
        state = context["state"]
        endpoint = "https://accounts.spotify.com/api/token"
        assert state == self.state
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        encoded_secret = encode_string_base64("{}:{}".format(client_id, client_secret))

        request_data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(encoded_secret),
        }
        response = self.send_post_request(endpoint, request_data, headers)
        response_json = response.json()
        self.access_token = response_json["access_token"]
        self.refresh_token = response_json["refresh_token"]
        self.headers = {
            "Authorization": "Bearer {}".format(self.access_token),
            "Content-Type": "application/json",
        }

    def _get_user_id(self) -> str:
        """
        Retrieve user_id from profile of Spotify user
        """

        response = self.send_get_request("https://api.spotify.com/v1/me", headers=self.headers)
        user_id = self._get_id_from_uri(response.json()["uri"])
        return user_id

    def _get_playlist(self, playlist_data: Dict[str, Any]) -> Playlist:
        """
        Create a `Playlist` object from the playlist data
        """

        playlist_title = playlist_data["name"]
        playlist_id = playlist_data["id"]
        endpoint = "https://api.spotify.com/v1/playlists/{}".format(playlist_id)
        params = {"fields": "tracks.items(track(name,artists))"}
        response = self.send_get_request(endpoint, params=params, headers=self.headers)
        response_json = response.json()
        songs: List[Song] = []
        for song in response_json["tracks"]["items"]:
            artists = [artist["name"] for artist in song["track"]["artists"]]
            song_title = song["track"]["name"]
            songs.append(Song(song_title, artists))
        playlist = Playlist(playlist_title, songs)
        return playlist
