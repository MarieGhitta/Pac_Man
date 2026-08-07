"""Define the possible contents of a maze cell."""


from enum import Enum, auto


class CellContent(Enum):
    """Represent the content of a maze cell."""

    EMPTY = auto()
    PACGUM = auto()
    SUPER_PACGUM = auto()
