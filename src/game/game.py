"""Manage the game."""

from src.config.models import Config
from src.game.level import Level


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configiration
        """
        self.config = config
        self.current_level_index = 0
        self.level = Level(config.levels[self.current_level_index],
                           config.seed)

    def run(self) -> None:
        """Run the game."""
        print("Game started!")