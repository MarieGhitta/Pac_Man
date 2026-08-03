"""Define states of ghosts."""

from enum import Enum, auto


class GhostState(Enum):
    FRIGHTENED = auto()
    DEAD = auto()
    CHASE = auto()
    SCATTER = auto()
    RESPAWN = auto()
