from typing import List
from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    """
    Serializer class for the Image object
    """

    url = serializers.CharField(max_length=200)
    height = serializers.IntegerField(default=0)
    width = serializers.IntegerField(default=0)


class SongSerializer(serializers.Serializer):
    """
    Serializer class for the Song object
    """

    title = serializers.CharField(max_length=200)
    artists = serializers.ListField(child=serializers.CharField(max_length=200))
    images = ImageSerializer(many=True)


class PlaylistSerializer(serializers.Serializer):
    """
    Serializer class for the Playlist object
    """

    title = serializers.CharField(max_length=200)
    songs = SongSerializer(many=True)
    images = ImageSerializer(many=True)
