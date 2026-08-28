"""Sprite state enums for the animation system."""


from enum import Enum, auto


class SpriteState(Enum):
    """Base class for all sprite animation states."""


class GhostState(SpriteState):
    """Represent differents states of ghosts."""

    FRIGHTENED = auto()
    CHASE = auto()
    SCATTER = auto()
    RESPAWN = auto()


class PacmanState(SpriteState):
    """Animation states for Pac-Man."""

    ALIVE = auto()
    DYING = auto()


class GhostType(Enum):
    """Represent the ghost types."""

    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()


class Direction(Enum):
    """Represent the possible movement directions."""

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
