from rest_framework.response import Response
from rest_framework.views import APIView

from playlistmover.playlistmover.models import Playlist, Song
from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.utils.clients import Spotify


class PlaylistApiView(APIView):
    """
    API View to manage retrieving and creating playlists from
    third-party music platforms for the caller.

    Authentication and Permissions are not required at this time.
    """

    def get(self, request, format=None):
        """
        Returns List of playlists from account and platform specified in the request.
        """
        request_data = request.data
        spotify = Spotify()
        playlists = spotify.get_playlists(request_data)
        serialised_playlist = PlaylistSerializer(playlists, many=True)
        return Response({"playlists": serialised_playlist.data})

    def post(self, request, format=None):
        """
        Creates List of playlists on account and platform specified in the request.
        """
        request_data = request.data
        playlists_data = request_data["playlists"]
        playlists = PlaylistSerializer(data=playlists_data, many=True)
        if playlists.is_valid():
            spotify = Spotify()
            created_playists = spotify.create_playlists(request_data, playlists)
            return Response({"success": True, "playlists": created_playists})
        return Response({"success": False, "playlists": []})
