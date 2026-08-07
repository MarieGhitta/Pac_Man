"""Define states of ghosts."""

from enum import Enum, auto


class GhostState(Enum):
    """Represent differents states of ghosts."""

    FRIGHTENED = auto()
    DEAD = auto()
    CHASE = auto()
    SCATTER = auto()
    RESPAWN = auto()
