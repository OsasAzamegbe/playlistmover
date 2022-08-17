from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from playlistmover.playlistmover.clients_enums import ClientEnum

from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.utils.clients import Client

from playlistmover.playlistmover.serializers import PlaylistSerializer

from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.utils.exceptions import (
    BadRequestException,
    get_exception_response,
)


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
        try:
            query_params = request.query_params
            platform: ClientEnum = query_params.get("platform")
            if platform:
                music_client = Client.get_client(platform)
                playlists = music_client.get_playlists(query_params)
                serialised_playlist = PlaylistSerializer(playlists, many=True)
                return Response(
                    {"success": True, "playlists": serialised_playlist.data}
                )
            raise BadRequestException("platform query parameter not specified")
        except Exception as exception:
            return get_exception_response(exception)

    def post(self, request, format=None):
        """
        Creates List of playlists on account and platform specified in the request.
        """
        try:
            request_data = request.data
            playlists_data = request_data["playlists"]
            playlists = PlaylistSerializer(data=playlists_data, many=True)
            if playlists.is_valid():
                music_client = Client.get_client(
                    request_data["context"]["platformEnum"]
                )
                created_playists = music_client.create_playlists(
                    request_data, playlists
                )
                return Response({"success": True, "playlists": created_playists})
            raise BadRequestException("`playlists` object in request is invalid")
        except Exception as exception:
            return get_exception_response(exception)


class AuthorizationRedirectView(APIView):
    """
    API View for providing authentication to the third-party music platform.
    """

    def get(self, request, format=None):
        """
        Initiate authentication and redirect
        """
        try:
            platform: ClientEnum = request.query_params.get("platform")
            if platform:
                music_client = Client.get_client(platform)
                url = music_client.get_authorization_url()
                return redirect(url)
            raise BadRequestException("platform query parameter not specified")
        except Exception as exception:
            return get_exception_response(exception)
