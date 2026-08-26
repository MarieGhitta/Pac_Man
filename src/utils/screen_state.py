from enum import Enum, auto


class ScreenState(Enum):
    TITLE = auto()
    CHEAT = auto()
    GAME = auto()
    PAUSE = auto()
    RESUME = auto()
    HIGHSCORE = auto()
    END = auto()
    QUIT = auto()
