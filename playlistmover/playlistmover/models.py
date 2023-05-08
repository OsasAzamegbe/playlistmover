"""
State models for objects used by this service
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Image:
    """
    Image object
    """

    url: str
    height: Optional[int]
    width: Optional[int]


@dataclass
class Song:
    """
    Song Object
    """

    title: str
    artists: list[str]
    images: list[Image]


@dataclass
class Playlist:
    """
    Playlist Object
    """

    title: str
    songs: list[Song]
    images: list[Image]
