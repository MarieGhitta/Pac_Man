"""Define states of ghosts."""

from enum import Enum, auto


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    DEAD = auto()
