"""Manage the game."""


import random

import pygame

from src.config.models import Config
from src.game.cell_content import CellContent
from src.game.direction import Direction
from src.game.level import Level
from src.game.player import Player
from src.game.ghost import Ghost
from src.game.ghost_state import GhostState
from src.game.ghost_type import GhostType
from src.maze.models import Cell


_PLAYER_UPDATE_DELAY: list[int] = [150, 133, 120, 120]
_GHOST_UPDATE_DELAY: dict[GhostState, list[int]] = {
    GhostState.SCATTER: [200, 175, 160, 160],
    GhostState.CHASE: [200, 175, 160, 160],
    GhostState.FRIGHTENED: [300, 275, 250, 250],
    GhostState.RESPAWN: [80,  80,  80, 80]
}
_GHOST_SCATTER_DELAY: list[list[float]] = [
    [7e3, 7e3, 5e3, 5e3],
    [7e3, 7e3, 5e3, 100/6],
    [5e3, 5e3, 5e3, 100/6],
    [5e3, 5e3, 5e3, 100/6]
]
_GHOST_CHASE_DELAY: list[list[float]] = [
    [2e4, 2e4, 2e4, float("inf")],
    [2e4, 2e4, 1033e3, float("inf")],
    [2e4, 2e4, 1037e3, float("inf")],
    [2e4, 2e4, 1037e3, float("inf")]
]
_GHOST_FRIGHTENED_DELAY: list[int] = [6000, 4000, 2000, 0]


class Game:
    """Represent the game."""

    def __init__(self, config: Config):
        """Initialize the game.

        Args:
            config (Config): The game configuration
        """
        self.config = config
        self.current_level_index: int = 0
        self.level: Level = Level(
            self.config.levels[self.current_level_index],
            self.config.seed,
            self.config.pacgum
        )
        current_time: int = pygame.time.get_ticks()
        self.player: Player = Player(
            self.level.start_cell.x,
            self.level.start_cell.y,
            current_time,
            _PLAYER_UPDATE_DELAY[0]
        )
        self.score: int = 0
        self.ghosts: list[Ghost] = self._create_ghosts(current_time)
        self.ghost_state: GhostState = GhostState.SCATTER
        self.global_ghosts_state: GhostState = GhostState.SCATTER
        self.state_phase_index: int = 0
        self.last_state_change: int = current_time
        self.lives: int = self.config.lives
        self.game_over: bool = False
        self.victory: bool = False
        self.elapsed_before_fright: int = 0
        self.is_frighten: bool = False
        self.eat_ghost_combo: int = 0

    def _create_ghosts(self, current_time: int) -> list[Ghost]:
        """Create the ghosts for the current level."""
        cells: list[Cell] = self.level.ghost_start_cells
        if len(cells) != 4:
            raise ValueError("expected four ghost start cells")
        return [
            self._ghost_factory(cells, 0, GhostType.BLINKY, current_time),
            self._ghost_factory(cells, 1, GhostType.PINKY, current_time),
            self._ghost_factory(cells, 2, GhostType.INKY, current_time),
            self._ghost_factory(cells, 3, GhostType.CLYDE, current_time)
        ]

    def _ghost_factory(
        self,
        cells: list[Cell],
        cell_idx: int,
        ghost_type: GhostType,
        current_time: int
    ) -> Ghost:
        """Create and return a Ghost from a cell list entry."""
        return Ghost(
            cells[cell_idx].x,
            cells[cell_idx].y,
            ghost_type,
            current_time,
            _GHOST_UPDATE_DELAY[GhostState.SCATTER][0]
        )

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
            self._frighten_ghosts()

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
            self.victory = True
            print("You win!")
            return
        self.level = Level(
            self.config.levels[self.current_level_index],
            random.randint(0, 2**32 - 1),
            self.config.pacgum
        )
        self.player.move_to(
            self.level.start_cell.x,
            self.level.start_cell.y
        )
        current_time = pygame.time.get_ticks()
        self.ghosts = self._create_ghosts(current_time)
        self.ghost_state = GhostState.SCATTER
        self.global_ghosts_state = GhostState.SCATTER
        self.state_phase_index = 0
        self.last_state_change = current_time
        self.player.last_update = current_time
        self.player.direction = Direction.LEFT
        self.player.next_direction = Direction.LEFT
        self.is_frighten = False
        self.elapsed_before_fright = 0

    def update(self) -> None:
        """Update the game state."""
        if self.game_over or self.victory:
            return
        current_time = pygame.time.get_ticks()
        self._update_ghost_state(current_time)
        if self.is_frighten:
            self._check_if_frighten(current_time)
        lvl_idx = self._level_interval()
        if (
            current_time - self.player.last_update
            >= _PLAYER_UPDATE_DELAY[lvl_idx]
        ):
            self.player.last_update = current_time
            self.player.prev_x = self.player.x
            self.player.prev_y = self.player.y
            self._update_player()
            self.player.update_delay = _PLAYER_UPDATE_DELAY[lvl_idx]
        for ghost in self.ghosts:
            if (
                current_time - ghost.last_update
                >= _GHOST_UPDATE_DELAY[ghost.state][lvl_idx]
            ):
                ghost.last_update = current_time
                ghost.prev_x = ghost.x
                ghost.prev_y = ghost.y
                ghost.update(
                    self.level,
                    self.player,
                    self.ghosts,
                    self.ghost_state,
                )
                ghost.update_delay = (
                    _GHOST_UPDATE_DELAY[ghost.state][lvl_idx]
                )
        self._check_collision()

    def _update_player(self) -> None:
        """Update the player."""
        self.move_player()

    def _level_interval(self) -> int:
        """Return the level interval."""
        if self.current_level_index == 0:
            return 0
        if self.current_level_index < 4:
            return 1
        if self.current_level_index < 10:
            return 2
        return 3

    def _update_ghost_state(self, current_time: int) -> None:
        """Update the ghosts state."""
        if self.is_frighten:
            return

        lvl_idx = self._level_interval()

        match self.ghost_state:
            case GhostState.SCATTER:
                delay = _GHOST_SCATTER_DELAY
            case GhostState.CHASE:
                delay = _GHOST_CHASE_DELAY
            case _:
                raise ValueError("unknown ghost state")
        if (
            current_time - self.last_state_change
            < delay[lvl_idx][self.state_phase_index]
        ):
            return

        self.last_state_change = current_time

        if self.ghost_state == GhostState.SCATTER:
            self.ghost_state = GhostState.CHASE
            self.global_ghosts_state = GhostState.CHASE
        else:
            self.ghost_state = GhostState.SCATTER
            self.global_ghosts_state = GhostState.SCATTER
            self.state_phase_index += 1

        for ghost in self.ghosts:
            if ghost.state == GhostState.FRIGHTENED:
                continue
            if ghost.state == GhostState.RESPAWN:
                continue
            ghost.state = self.ghost_state

    def _check_if_frighten(self, current_time: int) -> None:
        for ghost in self.ghosts:
            if ghost.state == GhostState.FRIGHTENED:
                return
        self.is_frighten = False
        self.last_state_change = current_time - self.elapsed_before_fright

    def _check_collision(self) -> None:
        """Check collisions between the player and the ghosts."""
        for ghost in self.ghosts:
            if ghost.state == GhostState.RESPAWN:
                continue
            if (ghost.x == self.player.x
               and ghost.y == self.player.y):
                self._handle_collision(ghost)
                return

    def _handle_collision(self, ghost: Ghost) -> None:
        """Handle a collision with a ghost."""
        if ghost.state == GhostState.FRIGHTENED:
            self._eat_ghost(ghost)
        else:
            self._player_hit()

    def _eat_ghost(self, ghost: Ghost) -> None:
        """Eat a frightened ghost."""
        score = self.config.points_per_ghost
        if self.eat_ghost_combo > 0:
            for _ in range(self.eat_ghost_combo):
                score *= 2
        self.eat_ghost_combo += 1
        self.score += score
        ghost.state = GhostState.RESPAWN

    def _player_hit(self) -> None:
        """Handle the player being hit."""
        self.lives -= 1
        if self.lives == 0:
            self.game_over = True
            print("Game Over")
            return
        self._reset_positions()

    def _reset_positions(self) -> None:
        """Reset the player and ghosts positions."""
        current_time = pygame.time.get_ticks()
        self.last_state_change = current_time
        self.player.move_to(
            self.level.start_cell.x,
            self.level.start_cell.y
        )
        self.ghost_state = GhostState.SCATTER
        self.global_ghosts_state = GhostState.SCATTER
        self.player.direction = Direction.LEFT
        self.player.next_direction = Direction.LEFT
        self.ghosts = self._create_ghosts(current_time)
        self.state_phase_index = 0
        self.is_frighten = False
        self.elapsed_before_fright = 0

    def _frighten_ghosts(self) -> None:
        """Put all ghosts in frightened state."""
        current_time = pygame.time.get_ticks()
        self.eat_ghost_combo = 0
        lvl_idx = self._level_interval()
        if lvl_idx == 3:
            return
        if not self.is_frighten:
            self.is_frighten = True
            self.elapsed_before_fright = current_time - self.last_state_change
        for ghost in self.ghosts:
            if ghost.state == GhostState.RESPAWN:
                continue
            ghost.state = GhostState.FRIGHTENED
            ghost.frightened_until = (
                current_time + _GHOST_FRIGHTENED_DELAY[lvl_idx]
            )

    def on_pause(self, current_time: int) -> None:
        self._pause_start = current_time

    def on_resume(self, current_time: int) -> None:
        duration = current_time - self._pause_start
        self.last_state_change += duration
        self.player.last_update += duration
        for ghost in self.ghosts:
            ghost.last_update += duration
