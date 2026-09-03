"""Manage a level."""


import random

from src.config.models import LevelConfig
from src.maze.generator import MazeFactory
from src.maze.models import Cell
from src.game.cell_content import CellContent


class Level:
    """Represent a game level: maze, pacgum placement, and start cells."""

    def __init__(
        self, level_config: LevelConfig, seed: int, pacgum_count: int
    ) -> None:
        """Generate the maze and initialize all cell contents.

        Args:
            level_config: Level dimensions.
            seed: RNG seed for maze generation.
            pacgum_count: Number of pacgums to place (0 = fill all).
        """
        self.level_config = level_config
        self.maze = MazeFactory().generate(
            self.level_config.width,
            self.level_config.height,
            seed
        )
        self.start_cell = self.player_start_cell()
        self.ghost_start_cells: list[Cell] = []
        self._initialize_contents(pacgum_count)

    def player_start_cell(self) -> Cell:
        """Return the player's starting cell."""
        center_x = self.maze.width // 2
        center_y = self.maze.height // 2
        cells_to_test = [(center_x, center_y)]
        if self.maze.width % 2 == 0:
            cells_to_test.append((center_x - 1, center_y))
        if self.maze.height % 2 == 0:
            cells_to_test.append((center_x, center_y - 1))
        if self.maze.width % 2 == 0 and self.maze.height % 2 == 0:
            cells_to_test.append((center_x - 1, center_y - 1))
        for x, y in cells_to_test:
            cell = self.maze.cells[y][x]
            if cell.walkable:
                return cell
        raise ValueError("the player starting cell is not walkable")

    def _initialize_contents(self, pacgum_count: int) -> None:
        """Initialize the contents of the maze cells.

        Args:
            pacgum_count: Number of pacgums to place (0 = fill all).
        """
        corner_cells = self._find_corner_cells()
        self.ghost_start_cells = corner_cells
        self._initialize_pacgums(pacgum_count, corner_cells)
        self._initialize_super_pacgums(corner_cells)
        self._clear_player_start()

    def _find_corner_cell(self, x_range: range, y_range: range) -> Cell:
        """Return the first walkable cell found scanning in the given ranges.

        Args:
            x_range: Column range to scan.
            y_range: Row range to scan.

        Returns:
            First walkable cell found.

        Raises:
            ValueError: If no walkable cell is found.
        """
        for y in y_range:
            for x in x_range:
                cell = self.maze.cells[y][x]
                if cell.walkable:
                    return cell
        raise ValueError("no walkable cell found")

    def _find_corner_cells(self) -> list[Cell]:
        """Return the four walkable corner cells, one per maze corner.

        Returns:
            List of four distinct corner cells.

        Raises:
            ValueError: If four distinct walkable corners cannot be found.
        """
        cells = [
            self._find_corner_cell(
                range(self.maze.width),
                range(self.maze.height)
            ),
            self._find_corner_cell(
                range(self.maze.width - 1, -1, -1),
                range(self.maze.height)
            ),
            self._find_corner_cell(
                range(self.maze.width),
                range(self.maze.height - 1, -1, -1)
            ),
            self._find_corner_cell(
                range(self.maze.width - 1, -1, -1),
                range(self.maze.height - 1, -1, -1)
            )
        ]
        if len(set(cells)) != 4:
            raise ValueError("could not determine four distinct corner cells")
        return cells

    def _initialize_pacgums(
        self, pacgum_count: int, corner_cells: list[Cell]
    ) -> None:
        """Place pacgums on walkable cells, excluding corners and player start.

        Args:
            pacgum_count: Number to place (0 or > available = fill all).
            corner_cells: Cells reserved for super-pacgums.
        """
        available_cells = []
        for row in self.maze.cells:
            for cell in row:
                if (
                    cell.walkable
                    and cell is not self.start_cell
                    and cell not in corner_cells
                ):
                    available_cells.append(cell)
        if pacgum_count < 1 or pacgum_count > len(available_cells):
            pacgum_count = len(available_cells)
        random.shuffle(available_cells)
        for cell in available_cells[:pacgum_count]:
            cell.content = CellContent.PACGUM

    def _initialize_super_pacgums(
        self, super_pacgum_cells: list[Cell]
    ) -> None:
        """Place a super-pacgum on each of the given cells.

        Args:
            super_pacgum_cells: Cells to mark as SUPER_PACGUM.
        """
        for cell in super_pacgum_cells:
            cell.content = CellContent.SUPER_PACGUM

    def _clear_player_start(self) -> None:
        """Clear the player's starting cell."""
        self.start_cell.content = CellContent.EMPTY
