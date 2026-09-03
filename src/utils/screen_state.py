"""Screen state enum for the application state machine."""


from enum import Enum, auto


class ScreenState(Enum):
    """Identifies the active screen or transition in the application loop."""

    TITLE = auto()
    CHEAT = auto()
    PAUSECHEAT = auto()
    GAME = auto()
    PAUSE = auto()
    RESUME = auto()
    HIGHSCORE = auto()
    END = auto()
    QUIT = auto()
