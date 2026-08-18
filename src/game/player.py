"""Manage Pac-Man."""


from src.game.direction import Direction


class Player:
    """Represent Pac-Man."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize Pac-Man."""
        self.x = x
        self.y = y
        self.prev_x: int = x
        self.prev_y: int = y
        self.direction: Direction = Direction.LEFT
        self.next_direction: Direction = Direction.LEFT

    def move_to(self, x: int, y: int) -> None:
        """Move the player to the given position."""
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
