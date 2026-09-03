"""Cheat flags container."""


class Cheat:
    """Hold all cheat mode flags for the current session."""

    def __init__(self) -> None:
        """Initialize all cheat flags to their default off state."""
        self.invincibility: bool = False
        self.ghost_freeze: bool = False
        self.speed_boost: bool = False
        self.infinite_time: bool = False
        self.infinite_lives: bool = False
        self.lvl_skip: bool = False
        self.add_lives: int = 0
        self.instant_win: bool = False
        self.instant_lose: bool = False
