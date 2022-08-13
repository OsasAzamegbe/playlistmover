from typing import Any, Dict, List
from playlistmover.playlistmover.models import Playlist, Song
from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.utils.enums import HTTPMethod


class Client(object):
    """
    HTTP client base-class
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_request(self, endpoint: str, request, method=HTTPMethod.GET):
        if method == HTTPMethod.GET:
            pass
        elif method == HTTPMethod.POST:
            pass


class Spotify(object):
    """
    Spotify Interface
    """

    def __init__(self):
        self.client = Client("www.spotify.com/api/")  # dummy endpoint

    def get_playlists(self, request) -> List[Playlist]:
        songs = [Song("Last last", "Burna Boy"), Song("Jailer", "Asa")]
        playlist = Playlist("naija", songs)
        playlist2 = Playlist("Afro beats", songs)
        return [playlist, playlist2]

    def create_playlists(
        self, request, playlists: PlaylistSerializer
    ) -> List[Dict[str, Any]]:
        print(playlists.create(playlists.validated_data))
        return playlists.validated_data
