"""Create maze."""


from src.game.cell_content import CellContent


class Cell:
    """Create Cell class."""

    def __init__(self,
                 x: int,
                 y: int,
                 north_wall: bool,
                 east_wall: bool,
                 south_wall: bool,
                 west_wall: bool,
                 walkable: bool) -> None:
        """Initialize a cell.

        Args:
            x (int): Coordinate x of a cell.
            y (int): Coordinate y of a cell.
            north_wall (bool): True if there is a north wall.
            east_wall (bool): True if there is a east wall.
            south_wall (bool): True if there is a south wall.
            west_wall (bool): True if there is a west wall.
            walkable (bool): True if the cell is not blocked.
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
