"""Manage the game."""

from src.config.models import Config
from src.maze.generator import MazeFactory


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configiration
        """
        self.config = config
        self.current_level_index = 0
        self.current_level = config.levels[self.current_level_index]
        self._generate_maze()

    def _generate_maze(self) -> None:
        """Generate the maze for the current level."""
        maze_factory = MazeFactory()
        self.maze = maze_factory.generate(self.current_level.width,
                                          self.current_level.height,
                                          self.config.seed)

    def run(self) -> None:
        """Run the game."""
        print("Game started!")