"""Manage Ghost."""


from src.game.ghost_state import GhostState
from src.game.direction import Direction


class Ghost:
    """Represent Ghost."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize Ghost."""
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.direction = Direction.UP
        self.state = GhostState.NORMAL
