"""Manage the game."""


import pygame
from src.config.models import Config
from src.game.level import Level
from src.game.player import Player
from src.game.direction import Direction
from src.game.cell_content import CellContent
from src.maze.models import Cell
from src.game.ghost import Ghost
from src.game.ghost_type import GhostType
from src.game.ghost_state import GhostState


_PLAYER_UPDATE_DELAY = 150
_GHOST_UPDATE_DELAY = 300
_GHOST_STATE_DELAY = 8000


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configuration
        """
        self.config = config
        self.current_level_index = 0
        self.level = Level(self.config.levels[self.current_level_index],
                           self.config.seed,
                           self.config.pacgum)
        self.player = Player(self.level.start_cell.x,
                             self.level.start_cell.y)
        self.score = 0
        self.ghosts = self._create_ghosts()
        current_time = pygame.time.get_ticks()
        self.last_player_update = current_time
        self.last_ghost_update = current_time
        self.ghost_state = GhostState.CHASE
        self.last_state_change = current_time

    def _create_ghosts(self) -> list[Ghost]:
        """Create the ghosts for the current level."""
        cells = self.level.ghost_start_cells
        if len(cells) != 4:
            raise ValueError("Expected four ghost start cells.")
        return [
            Ghost(cells[0].x, cells[0].y, GhostType.BLINKY),
            Ghost(cells[1].x, cells[1].y, GhostType.PINKY),
            Ghost(cells[2].x, cells[2].y, GhostType.INKY),
            Ghost(cells[3].x, cells[3].y, GhostType.CLYDE)
        ]

    def _can_move(self, direction: Direction) -> bool:
        """Return whether the player can move in the given direction."""
        current_cell = self.level.maze.cells[self.player.y][self.player.x]
        if direction == Direction.UP:
            return not current_cell.north_wall
        if direction == Direction.RIGHT:
            return not current_cell.east_wall
        if direction == Direction.DOWN:
            return not current_cell.south_wall
        if direction == Direction.LEFT:
            return not current_cell.west_wall
        return False

    def move_player(self) -> None:
        """Move the player in the given direction."""
        if self._can_move(self.player.next_direction):
            self.player.direction = self.player.next_direction
        if not self._can_move(self.player.direction):
            return
        if self.player.direction == Direction.UP:
            self.player.y -= 1
        elif self.player.direction == Direction.RIGHT:
            self.player.x += 1
        elif self.player.direction == Direction.DOWN:
            self.player.y += 1
        elif self.player.direction == Direction.LEFT:
            self.player.x -= 1
        new_cell = self.level.maze.cells[self.player.y][self.player.x]
        self._collect_cell_content(new_cell)
        if self._is_level_completed():
            self._next_level()

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

    def _next_level(self) -> None:
        """Load the next level."""
        self.current_level_index += 1
        if self.current_level_index >= len(self.config.levels):
            print("You win!")
            return
        self.level = Level(
            self.config.levels[self.current_level_index],
            self.config.seed,
            self.config.pacgum)
        self.player.move_to(self.level.start_cell.x,
                            self.level.start_cell.y)
        self.ghosts = self._create_ghosts()
        current_time = pygame.time.get_ticks()
        self.ghost_state = GhostState.CHASE
        self.last_state_change = current_time
        self.last_player_update = current_time
        self.last_ghost_update = current_time
        self.player.direction = Direction.NONE
        self.player.next_direction = Direction.NONE

    def update(self) -> None:
        """Update the game state."""
        current_time = pygame.time.get_ticks()
        self._update_ghost_state(current_time)
        if current_time - self.last_player_update >= _PLAYER_UPDATE_DELAY:
            self.last_player_update = current_time
            self._update_player()
        if current_time - self.last_ghost_update >= _GHOST_UPDATE_DELAY:
            self.last_ghost_update = current_time
            self._update_ghosts()
        # self._check_collision()

    def _update_ghosts(self) -> None:
        """Update all ghosts."""
        for ghost in self.ghosts:
            ghost.update(self.level, self.player)

    def _update_player(self) -> None:
        """Update the player."""
        self.move_player()

    def _update_ghost_state(self, current_time: int) -> None:
        """Update the ghosts state."""
        if current_time - self.last_state_change < _GHOST_STATE_DELAY:
            return
        self.last_state_change = current_time
        if self.ghost_state == GhostState.CHASE:
            self.ghost_state = GhostState.SCATTER
        else:
            self.ghost_state = GhostState.CHASE
        for ghost in self.ghosts:
            ghost.state = self.ghost_state
