"""Manage a level."""

from src.config.models import LevelConfig
from src.maze.generator import MazeFactory
from src.maze.models import Cell


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

    def player_start_cell(self) -> Cell:
        """Return the player's starting cell."""
        center_x = self.maze.width // 2
        center_y = self.maze.height // 2
        cells_to_test = [(center_x, center_y)]
        if self.maze.width % 2 == 0:
            cells_to_test.append((center_x - 1, center_y))
        if self.maze.height % 2 == 0:
            cells_to_test.append((center_x, center_y - 1))
        if self.maze.width % 2 and self.maze.height % 2 == 0:
            cells_to_test.append((center_x - 1, center_y - 1))
        for x, y in cells_to_test:
            cell = self.maze.cells[y][x]
            if cell.walkable:
                return cell
        raise ValueError("The player starting cell is not walkable.")
        
