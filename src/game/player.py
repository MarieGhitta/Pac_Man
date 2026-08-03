"""Manage Pac-Man."""

from src.game.direction import Direction


class Player:
    """Represent Pac-Man."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize Pac-Man."""
        self.x = x
        self.y = y
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE

    def move_to(self, x: int, y: int) -> None:
        """Move the player to the given position."""
        self.x = x
        self.y = y

