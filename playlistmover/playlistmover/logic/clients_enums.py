from enum import Enum


class ClientEnum(str, Enum):
    """
    Enum of supported Client interfaces
    """

    SPOTIFY = "SPOTIFY"
    APPLE_MUSIC = "APPLE_MUSIC"
    YOUTUBE_MUSIC = "YOUTUBE_MUSIC"

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return

        for member in cls:
            if member.name.upper() == value.upper():
                return member
