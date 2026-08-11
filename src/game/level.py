"""Manage a level."""

import random
from src.config.models import LevelConfig
from src.maze.generator import MazeFactory
from src.maze.models import Cell
from src.game.cell_content import CellContent


class Level:
    """Represent a level."""

    def __init__(
        self,
        level_config: LevelConfig,
        seed: int,
        pacgum_count: int
    ):
        """Initialize a level.

        Args:
            level_config (LevelConfig): configuration of the level.
            seed (int): seed.
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
        if self.maze.width % 2 and self.maze.height % 2 == 0:
            cells_to_test.append((center_x - 1, center_y - 1))
        for x, y in cells_to_test:
            cell = self.maze.cells[y][x]
            if cell.walkable:
                return cell
        raise ValueError("The player starting cell is not walkable.")

    def _initialize_contents(self, pacgum_count: int) -> None:
        """Initialize the contents of the maze cells."""
        corner_cells = self._find_corner_cells()
        self.ghost_start_cells = corner_cells
        self._initialize_pacgums(pacgum_count, corner_cells)
        self._initialize_super_pacgums(corner_cells)
        self._clear_player_start()

    def _find_corner_cell(self, x_range: range, y_range: range) -> Cell:
        """Return first walkable cell found when searching from a corner."""
        for y in y_range:
            for x in x_range:
                cell = self.maze.cells[y][x]
                if cell.walkable:
                    return cell
        raise ValueError("No walkable cell found.")

    def _find_corner_cells(self) -> list[Cell]:
        """Return the four walkable corner cells."""
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
            raise ValueError("Could not determine four distinct corner cells.")
        return cells

    def _initialize_pacgums(
            self,
            pacgum_count: int,
            corner_cells: list[Cell]
    ) -> None:
        """Place the pacgums in the maze."""
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

    def _initialize_super_pacgums(self,
                                  super_pacgum_cells: list[Cell]) -> None:
        """Place the super pacgums in the maze."""
        for cell in super_pacgum_cells:
            cell.content = CellContent.SUPER_PACGUM

    def _clear_player_start(self) -> None:
        """Clear the player's starting cell."""
        self.start_cell.content = CellContent.EMPTY
