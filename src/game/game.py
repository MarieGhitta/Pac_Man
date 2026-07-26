"""Manage the game."""

from src.config.models import Config
from src.game.level import Level
from src.game.player import Player
from src.game.direction import Direction


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configuration
        """
        self.config = config
        self.current_level_index = 0
        self.level = Level(config.levels[self.current_level_index],
                           config.seed)
        start_cell = self.level.player_start_cell()
        self.player = Player(start_cell.x,
                             start_cell.y)

    def run(self) -> None:
        """Run the game."""
        print("Game started!")

    def move_player(self, direction: Direction) -> None:
        """Move the player in the given direction."""
        current_cell = self.level.maze.cells[self.player.y][self.player.x]
        if direction == Direction.UP:
            if not current_cell.north_wall:
                self.player.y -= 1
        elif direction == Direction.RIGHT:
            if not current_cell.east_wall:
                self.player.x += 1
        elif direction == Direction.DOWN:
            if not current_cell.south_wall:
                self.player.y += 1
        elif direction == Direction.LEFT:
            if not current_cell.west_wall:
                self.player.x -= 1
