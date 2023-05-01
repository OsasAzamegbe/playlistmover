from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from playlistmover.playlistmover.logic.clients_enums import ClientEnum

from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.logic.clients import Client

from playlistmover.playlistmover.serializers import PlaylistSerializer

from playlistmover.playlistmover.serializers import PlaylistSerializer
from playlistmover.playlistmover.logic.exceptions import (
    BadRequestException,
    get_exception_response,
)
from playlistmover.playlistmover.logic.validator import request_validator


class PlaylistApiView(APIView):
    """
    API View to manage retrieving and creating playlists from
    third-party music platforms for the caller.
    """

    @request_validator("getPlaylists")
    def get(self, request, format=None):
        """
        Returns List of playlists from account and platform specified in the request.
        """
        try:
            query_params = request.query_params
            platform = ClientEnum(query_params["platform"])
            redirect_uri = request.query_params["redirect_uri"]
            music_client = Client.get_client(platform)
            playlists = music_client.get_playlists(query_params, redirect_uri)
            serialised_playlist = PlaylistSerializer(playlists, many=True)
            return Response({"success": True, "playlists": serialised_playlist.data})
        except Exception as exception:
            return get_exception_response(exception)

    @request_validator("postPlaylists")
    def post(self, request, format=None):
        """
        Creates List of playlists on account and platform specified in the request.
        """
        try:
            request_data = request.data
            playlists_data = request_data["playlists"]
            playlists = PlaylistSerializer(data=playlists_data, many=True)
            if playlists.is_valid():
                platform = ClientEnum(request_data["context"]["platform"])
                music_client = Client.get_client(platform)
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

    @request_validator("getAuth")
    def get(self, request, format=None):
        """
        Initialise and return platform account authentication url.
        """
        try:
            platform = ClientEnum(request.query_params["platform"])
            redirect_uri = request.query_params["redirect_uri"]
            music_client = Client.get_client(platform)
            url = music_client.get_authorization_url(redirect_uri)
            return Response({"success": True, "auth_url": url})
        except Exception as exception:
            return get_exception_response(exception)
