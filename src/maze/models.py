"""Create maze."""


from src.game.cell_content import CellContent


class Cell:
    """Represent a single maze tile with wall flags and content."""

    def __init__(
        self,
        x: int,
        y: int,
        north_wall: bool,
        east_wall: bool,
        south_wall: bool,
        west_wall: bool,
        walkable: bool
    ) -> None:
        """Initialize a maze cell.

        Args:
            x: Tile column.
            y: Tile row.
            north_wall: True if a north wall is present.
            east_wall: True if an east wall is present.
            south_wall: True if a south wall is present.
            west_wall: True if a west wall is present.
            walkable: True if the cell can be entered.
        """
        self.x = x
        self.y = y
        self.north_wall = north_wall
        self.east_wall = east_wall
        self.south_wall = south_wall
        self.west_wall = west_wall
        self.walkable = walkable
        self.content = CellContent.EMPTY


class Maze:
    """Represent the full maze grid with entry and exit references."""

    def __init__(
        self,
        width: int,
        height: int,
        cells: list[list[Cell]],
        entry_cell: Cell,
        exit_cell: Cell
    ) -> None:
        """Initialize the maze.

        Args:
            width: Number of tile columns.
            height: Number of tile rows.
            cells: 2D grid of Cell instances.
            entry_cell: Maze entry cell.
            exit_cell: Maze exit cell.
        """
        self.width = width
        self.height = height
        self.cells = cells
        self.entry_cell = entry_cell
        self.exit_cell = exit_cell
