"""Create class MazeGenerator."""


from mazegenerator import MazeGenerator as LibMazeGenerator

from .adapter import MazeAdapter
from .models import Maze


class MazeFactory:
    """Generate Maze objects from the external maze generator."""

    def generate(self, width: int, height: int, seed: int) -> Maze:
        """Generate and adapt a maze.

        Args:
            width: Width of the maze in tiles.
            height: Height of the maze in tiles.
            seed: RNG seed for maze generation.

        Returns:
            Adapted Maze instance.
        """
        generator = LibMazeGenerator(
            size=(width, height), perfect=False, seed=seed
        )
        adapter = MazeAdapter()

        return adapter.adapt(
            generator.maze, generator.maze_entry, generator.maze_exit
        )
