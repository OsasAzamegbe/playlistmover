from enum import Enum
from pdb import post_mortem
from pickle import GET


class HTTPMethod(Enum):
    GET = 0
    POST = 1
