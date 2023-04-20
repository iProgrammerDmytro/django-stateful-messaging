from enum import Enum


class ChatType(Enum):
    """
    Chat communication via.
    """
    DEFAULT = "Default"
    WHATS_APP = "WhatsApp"


class Module(Enum):
    """
    Algorithms/modules for users.
    """
    BGCHECK = "BGCHECK"
