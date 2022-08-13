from typing import List
from rest_framework import serializers

from playlistmover.playlistmover.models import Playlist, Song


class SongSerializer(serializers.Serializer):
    """
    Serializer class for the Song object
    """

    title = serializers.CharField(max_length=200)
    artist = serializers.CharField(max_length=200)


class PlaylistSerializer(serializers.Serializer):
    """
    Serializer class for the Playlist object
    """

    title = serializers.CharField(max_length=200)
    songs = SongSerializer(many=True)

    def create(self, validated_data):
        songs: List[Song] = validated_data.get("songs")
        songs = [Song(**song) for song in songs]
        return Playlist(title=validated_data["title"], songs=songs)
