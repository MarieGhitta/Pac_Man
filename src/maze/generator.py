"""Create class MazeGenerator."""
from mazegenerator import MazeGenerator as LibMazeGenerator


class MazeFactory:
    """Generate MazeGenerator object."""

    def generate(self,
                 width: int,
                 height: int,
                 seed: int) -> tuple[list[list[int]],
                                     tuple[int, int],
                                     tuple[int, int]]:
        """Generate maze.

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
        return (generator.maze,
                generator.maze_entry,
                generator.maze_exit)
