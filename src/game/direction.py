"""Define movement directions used in the game."""


from enum import Enum, auto


class Direction(Enum):
    """Represent the possible movement directions."""

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()