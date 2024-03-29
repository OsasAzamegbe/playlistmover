import os
from typing import Any, Dict, List, Optional
import requests
from requests.models import PreparedRequest
from rest_framework.status import HTTP_200_OK

from playlistmover.playlistmover.logic.clients_enums import ClientEnum
from playlistmover.playlistmover.models import Playlist, Song
from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.logic.exceptions import (
    BadRequestException,
    UnauthorizedException,
)
from playlistmover.playlistmover.logic.utils import encode_string_base64


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
        return requests.get(
            "{}{}".format(self.base_url, endpoint), params=params, headers=headers
        )

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
        raise BadRequestException("`{}` not supported.".format(client_enum))


class SpotifyClient(Client):
    """
    Spotify Client Interface
    """

    def __init__(self):
        self.state = "123456789abcdefg"
        self.access_token = self.refresh_token = ""
        self.headers = {}
        super().__init__()

    @staticmethod
    def _get_id_from_uri(uri: str) -> str:
        """
        Parse the `id` from a spotify uri of the form spotify:type:id
        """
        return uri.split(":")[-1]

    def get_playlists(
        self, context: Dict[str, str], redirect_uri: str
    ) -> List[Playlist]:
        """
        Get list of playlists from Spotify account
        """
        self._setup_auth_tokens(context, redirect_uri)
        user_id = self._get_user_id()
        endpoint = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        params = {"limit": 50}
        response = self.send_get_request(endpoint, params=params, headers=self.headers)
        response_json = response.json()
        playlists: List[Playlist] = [
            self._get_playlist(playlist) for playlist in response_json["items"]
        ]
        return playlists

    def create_playlists(
        self, request, playlists: PlaylistSerializer
    ) -> List[Dict[str, Any]]:
        """
        Create list of playlists on Spotify account
        """
        print(playlists.create(playlists.validated_data))
        return playlists.validated_data

    def get_authorization_url(self, redirect_uri: str) -> str:
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
            "redirect_uri": redirect_uri,
            "state": self.state,
        }
        req_builder.prepare_url(url, params)
        return req_builder.url

    def _setup_auth_tokens(self, context: Dict[str, str], redirect_uri: str):
        """
        get authentication options after setting up initial authentication with Spotify
        """
        code = context["code"]
        state = context["state"]
        endpoint = "https://accounts.spotify.com/api/token"
        if state != self.state:
            raise UnauthorizedException("User is unauthorized.")
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        encoded_secret = encode_string_base64("{}:{}".format(client_id, client_secret))

        request_data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(encoded_secret),
        }
        response = self.send_post_request(endpoint, request_data, headers)
        response_json = response.json()

        if (
            response.status_code != HTTP_200_OK
            or "access_token" not in response_json
            or "refresh_token" not in response_json
        ):
            raise UnauthorizedException("User is unauthorized.", response_json)
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

        response = self.send_get_request(
            "https://api.spotify.com/v1/me", headers=self.headers
        )
        user_id = self._get_id_from_uri(response.json()["uri"])
        return user_id

    def _get_playlist(self, playlist_data: Dict[str, Any]) -> Playlist:
        """
        Create a `Playlist` object from the playlist data
        """
        playlist_title = playlist_data["name"]
        playlist_id = playlist_data["id"]
        endpoint = "https://api.spotify.com/v1/playlists/{}".format(playlist_id)
        params = {
            "fields": "images,tracks.items(track(name,artists(name),album(images)))"
        }
        response = self.send_get_request(endpoint, params=params, headers=self.headers)
        response_json = response.json()
        songs: List[Song] = []
        for song in response_json["tracks"]["items"]:
            if not song or not song.get("track"):
                continue
            artists = [
                artist.get("name", "") for artist in song["track"].get("artists", [])
            ]
            song_title = song["track"]["name"]
            songs.append(
                Song(
                    song_title,
                    artists,
                    song["track"].get("album", {}).get("images", []),
                )
            )
        playlist = Playlist(playlist_title, songs, response_json.get("images", []))
        return playlist
