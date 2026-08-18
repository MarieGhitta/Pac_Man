"""Manage Ghost."""


import random
import math

import pygame

from src.game.ghost_state import GhostState
from src.game.direction import Direction
from src.game.player import Player
from src.game.level import Level
from src.game.ghost_type import GhostType


class Ghost:
    """Represent a Ghost."""

    def __init__(
        self, x: int, y: int, ghost_type: GhostType, last_update: int
    ) -> None:
        """Initialize Ghost."""
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.direction = Direction.UP
        self.state = GhostState.SCATTER
        self.frightened_until = 0
        self.ghost_type = ghost_type
        self.last_update = last_update

    def update(
        self,
        level: Level,
        player: Player,
        ghosts: list["Ghost"],
        current_state: GhostState
    ) -> None:
        """Update the ghost."""
        current_time = pygame.time.get_ticks()
        if (
            self.state == GhostState.FRIGHTENED
            and current_time >= self.frightened_until
        ):
            self.state = current_state
        self.direction = self._choose_direction(level, player, ghosts)
        self._move(level)
        if (
            self.state == GhostState.RESPAWN
            and (self.x, self.y) == (level.start_cell.x, level.start_cell.y)
        ):
            self.state = current_state

    def _choose_direction(
        self, level: Level, player: Player, ghosts: list["Ghost"]
    ) -> Direction:
        """Choose the next direction."""
        directions = self._possible_directions(level)
        directions = self._remove_opposite_direction(directions)
        match self.state:
            case GhostState.SCATTER:
                return self._choose_scatter_direction(directions)
            case GhostState.CHASE:
                return self._choose_chase_direction(directions, player, ghosts)
            case GhostState.FRIGHTENED:
                return self._choose_frightened_direction(directions)
            case GhostState.RESPAWN:
                return self._choose_respawn_direction(directions, level)

    def _possible_directions(self, level: Level) -> list[Direction]:
        """Return all possible movement directions."""
        current_cell = level.maze.cells[self.y][self.x]
        directions = []
        if not current_cell.north_wall:
            directions.append(Direction.UP)
        if not current_cell.east_wall:
            directions.append(Direction.RIGHT)
        if not current_cell.south_wall:
            directions.append(Direction.DOWN)
        if not current_cell.west_wall:
            directions.append(Direction.LEFT)
        return directions

    def _move(self, level: Level) -> None:
        """Move the ghost in its current direction."""
        current_cell = level.maze.cells[self.y][self.x]
        if self.direction == Direction.UP:
            if not current_cell.north_wall:
                self.y -= 1
        elif self.direction == Direction.RIGHT:
            if not current_cell.east_wall:
                self.x += 1
        elif self.direction == Direction.DOWN:
            if not current_cell.south_wall:
                self.y += 1
        elif self.direction == Direction.LEFT:
            if not current_cell.west_wall:
                self.x -= 1

    def _next_position(self, direction: Direction) -> tuple[int, int]:
        """Return the next position for the given direction."""
        if direction == Direction.UP:
            return self.x, self.y - 1
        if direction == Direction.RIGHT:
            return self.x + 1, self.y
        if direction == Direction.DOWN:
            return self.x, self.y + 1
        if direction == Direction.LEFT:
            return self.x - 1, self.y

    def _choose_target_direction(
        self, directions: list[Direction], target_x: int, target_y: int
    ) -> Direction:
        """Choose the direction that gets closest to the target."""
        best_directions = []
        best_distance = float("inf")
        for direction in directions:
            next_x, next_y = self._next_position(direction)
            distance = math.hypot(target_x - next_x, target_y - next_y)
            if distance < best_distance:
                best_distance = distance
                best_directions = [direction]
            elif distance == best_distance:
                best_directions.append(direction)
        return random.choice(best_directions)

    def _choose_chase_direction(
        self,
        directions: list[Direction],
        player: Player,
        ghosts: list["Ghost"]
    ) -> Direction:
        """Choose the direction that gets closest to the player."""
        target_x, target_y = self._target_position(player, ghosts)
        return self._choose_target_direction(directions, target_x, target_y)

    def _choose_scatter_direction(
        self, directions: list[Direction]
    ) -> Direction:
        """Choose the direction that gets closest to the spawn."""
        return self._choose_target_direction(
            directions, self.spawn_x, self.spawn_y
        )

    def _choose_frightened_direction(
        self, directions: list[Direction]
    ) -> Direction:
        """Choose a random direction."""
        return random.choice(directions)

    def _choose_respawn_direction(
        self, directions: list[Direction], level: Level
    ) -> Direction:
        """Choose the direction that gets closest to the spawn."""
        return self._choose_target_direction(
            directions, level.start_cell.x, level.start_cell.y
        )

    def _opposite_direction(self) -> Direction:
        if self.direction == Direction.UP:
            return Direction.DOWN
        if self.direction == Direction.RIGHT:
            return Direction.LEFT
        if self.direction == Direction.DOWN:
            return Direction.UP
        if self.direction == Direction.LEFT:
            return Direction.RIGHT
        raise ValueError("invalid direction")

    def _remove_opposite_direction(
        self, directions: list[Direction]
    ) -> list[Direction]:
        """Remove the opposite direction if another direction is available."""
        remaining_directions = []
        if len(directions) == 1:
            return directions
        opposite = self._opposite_direction()
        for direction in directions:
            if direction != opposite:
                remaining_directions.append(direction)
        return remaining_directions

    def _target_position(
        self, player: Player, ghosts: list["Ghost"]
    ) -> tuple[int, int]:
        """Return the target position."""
        match self.ghost_type:
            case GhostType.BLINKY:
                return player.x, player.y
            case GhostType.PINKY:
                return self._position_ahead(player, 4)
            case GhostType.INKY:
                pivot = self._position_ahead(player, 2)
                blinky = next(
                    g for g in ghosts if g.ghost_type == GhostType.BLINKY
                )
                return pivot[0] * 2 - blinky.x, pivot[1] * 2 - blinky.y
            case GhostType.CLYDE:
                if math.hypot(self.x - player.x, self.y - player.y) >= 8:
                    return player.x, player.y
                else:
                    return self.spawn_x, self.spawn_y

    def _position_ahead(self, player: Player, n: int) -> tuple[int, int]:
        """Return the position n cell ahead of the player."""
        match player.direction:
            case Direction.UP:
                return player.x - n, player.y - n
            case Direction.DOWN:
                return player.x, player.y + n
            case Direction.LEFT:
                return player.x - n, player.y
            case Direction.RIGHT:
                return player.x + n, player.y
