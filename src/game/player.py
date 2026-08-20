"""Manage Pac-Man."""


from src.game.direction import Direction


class Player:
    """Represent Pac-Man."""

    def __init__(
        self, x: int, y: int, last_update: int, update_delay: int
    ) -> None:
        """Initialize Pac-Man.

        Args:
            x: Starting tile column.
            y: Starting tile row.
        """
        self.x = x
        self.y = y
        self.last_update = last_update
        self.update_delay = update_delay
        self.prev_x: int = x
        self.prev_y: int = y
        self.direction: Direction = Direction.LEFT
        self.next_direction: Direction = Direction.LEFT

    def move_to(self, x: int, y: int) -> None:
        """Move the player to the given tile position.

        Resets prev_x and prev_y to the new position to prevent
        interpolation across the jump.

        Args:
            x: Target tile column.
            y: Target tile row.
        """
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
