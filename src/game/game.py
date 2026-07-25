"""Manage the game."""

from src.config.models import Config
from src.game.level import Level
from src.game.player import Player


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