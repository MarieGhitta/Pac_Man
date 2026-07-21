"""Create maze."""


class Cell:
    """Create Cell class."""

    def __init__(self,
                 x: int,
                 y: int,
                 north_open: bool,
                 east_open: bool,
                 south_open: bool,
                 west_open: bool) -> None:
        """Initialize a cell.

        Args:
            x (int): Coordinate x of a cell.
            y (int): Coordinate y of a cell.
            north_open (bool): True if north wall is open.
            east_open (bool): True if east wall is open.
            south_open (bool): True if south wall is open.
            west_open (bool): True if west wall is open.
        """
        self.x = x
        self.y = y
        self.north_open = north_open
        self.east_open = east_open
        self.south_open = south_open
        self.west_open = west_open


class Maze:
    """Create Maze class."""

    def __init__(self,
                 width: int,
                 height: int,
                 cells: list[list[Cell]],
                 entry_cell: Cell,
                 exit_cell: Cell) -> None:
        """Initialize maze class.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze
            cells (list[list[Cell]]): Cells of the maze.
            entry_cell (Cell): Entry of the maze.
            exit_cell (Cell): Exit of the maze.
        """
        self.width = width
        self.height = height
        self.cells = cells
        self.entry_cell = entry_cell
        self.exit_cell = exit_cell
