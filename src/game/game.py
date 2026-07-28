"""Manage the game."""

from src.config.models import Config
from src.game.level import Level
from src.game.player import Player
from src.game.direction import Direction
from src.game.cell_content import CellContent
from src.maze.models import Cell


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configuration
        """
        self.config = config
        self.current_level_index = 0
        self.level = Level(config.levels[self.current_level_index],
                           config.seed,
                           config.pacgum)
        self.player = Player(self.level.start_cell.x,
                             self.level.start_cell.y)
        self.score = 0

    def run(self) -> None:
        """Run the game."""
        print("Game started!")

    def move_player(self, direction: Direction) -> None:
        """Move the player in the given direction."""
        current_cell = self.level.maze.cells[self.player.y][self.player.x]
        if direction == Direction.UP:
            if not current_cell.north_wall:
                self.player.y -= 1
        elif direction == Direction.RIGHT:
            if not current_cell.east_wall:
                self.player.x += 1
        elif direction == Direction.DOWN:
            if not current_cell.south_wall:
                self.player.y += 1
        elif direction == Direction.LEFT:
            if not current_cell.west_wall:
                self.player.x -= 1
        new_cell = self.level.maze.cells[self.player.y][self.player.x]
        self._collect_cell_content(new_cell)
        if self._is_level_completed():
            print("Level completed!") 

    def _collect_cell_content(self, cell: Cell) -> None:
        """Collect the content of a maze cell."""
        if cell.content == CellContent.PACGUM:
            cell.content = CellContent.EMPTY
            self.score += self.config.points_per_pacgum
        elif cell.content == CellContent.SUPER_PACGUM:
            cell.content = CellContent.EMPTY
            self.score += self.config.points_per_super_pacgum

    def _is_level_completed(self) -> bool:
        """Return True if the current level is completed."""
        for row in self.level.maze.cells:
            for cell in row:
                if (cell.content == CellContent.PACGUM
                   or cell.content == CellContent.SUPER_PACGUM):
                    return False
        return True
