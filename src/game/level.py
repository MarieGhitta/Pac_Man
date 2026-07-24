"""Manage a level."""

from src.config.models import LevelConfig
from src.maze.generator import MazeFactory


class Level:
    """Represent a level."""

    def __init__(self, level_config: LevelConfig, seed: int):
        """Initialize a level.

        Args:
            level_config (LevelConfig): configuration of the level.
            seed (int): seed.
        """
        self.level_config = level_config
        self.maze = MazeFactory().generate(
            self.level_config.width,
            self.level_config.height,
            seed)
