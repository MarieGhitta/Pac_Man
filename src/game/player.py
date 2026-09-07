"""Manage Pac-Man."""


from src.utils.sprite_enums import Direction


class Player:
    """Represent the player-controlled Pac-Man entity."""

    def __init__(self, x: int, y: int, last_update: int) -> None:
        """Initialize Pac-Man at a given tile position.

        Args:
            x: Starting tile column.
            y: Starting tile row.
            last_update: Timestamp of the last movement tick.
        """
        self.x = x
        self.y = y
        self.last_update = last_update
        self.render_x: float = float(x)
        self.render_y: float = float(y)
        self.direction: Direction = Direction.LEFT
        self.next_direction: Direction = Direction.LEFT

    def move_to(self, x: int, y: int) -> None:
        """Move the player to the given tile position.

        Args:
            x: Target tile column.
            y: Target tile row.
        """
        self.x = x
        self.y = y
        self.render_x = float(x)
        self.render_y = float(y)
