"""
State models for objects used by this service
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    """
    Song Object
    """

    title: str
    artists: List[str]


@dataclass
class Playlist:
    """
    Playlist Object
    """

    title: str
    songs: List[Song]
