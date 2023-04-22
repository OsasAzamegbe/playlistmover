from enum import Enum


class ClientEnum(str, Enum):
    """
    Enum of supported Client interfaces
    """

    SPOTIFY = "SPOTIFY"
    APPLE_MUSIC = "APPLE_MUSIC"
    YOUTUBE_MUSIC = "YOUTUBE_MUSIC"
