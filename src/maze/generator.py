"""Create class MazeGenerator."""
from mazegenerator import MazeGenerator as LibMazeGenerator

from .adapter import MazeAdapter
from .models import Maze


class MazeFactory:
    """Generate Maze objects from the external maze generator."""

    def generate(self,
                 width: int,
                 height: int,
                 seed: int) -> Maze:
        """Generate and adapt a maze.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
            seed (int): Seed of the maze.

        Returns:
            tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
            Generated maze, coordinates entry cell, coordinates exit cell.
        """
        generator = LibMazeGenerator(size=(width, height),
                                     perfect=False,
                                     seed=seed)
        adapter = MazeAdapter()

        return adapter.adapt(generator.maze,
                             generator.maze_entry,
                             generator.maze_exit)
