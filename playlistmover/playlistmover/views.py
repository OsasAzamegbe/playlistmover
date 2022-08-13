from rest_framework.response import Response
from rest_framework.views import APIView


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
        return Response({"playlists": []})

    def post(self, request, format=None):
        """
        Creates List of playlists on account and platform specified in the request.
        """
        return Response({"success": True})
