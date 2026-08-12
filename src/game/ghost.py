"""Manage Ghost."""

import pygame
import random
from src.game.ghost_state import GhostState
from src.game.direction import Direction
from src.game.player import Player
from src.game.level import Level
from src.game.ghost_type import GhostType


class Ghost:
    """Represent Ghost."""

    def __init__(self, x: int, y: int, ghost_type: GhostType) -> None:
        """Initialize Ghost."""
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.direction = Direction.UP
        self.state = GhostState.SCATTER
        self.frightened_until = 0.0
        self.respawn_until = 0.0
        self.ghost_type = ghost_type

    def update(
        self, level: Level, player: Player, normal_state: GhostState
    ) -> None:
        """Update the ghost."""
        current_time = pygame.time.get_ticks()
        if (
            self.state == GhostState.FRIGHTENED
            and current_time >= self.frightened_until
        ):
            self.state = normal_state
        self.direction = self._choose_direction(level, player)
        self._move(level)
        if (
            self.state == GhostState.RESPAWN
            and current_time >= self.respawn_until
            and self.x == self.spawn_x
            and self.y == self.spawn_y
        ):
            self.state = normal_state

    def _choose_direction(self, level: Level, player: Player) -> Direction:
        """Choose the next direction."""
        directions = self._possible_directions(level)
        directions = self._remove_opposite_direction(directions)
        if self.state == GhostState.CHASE:
            return self._choose_chase_direction(directions, player)
        if self.state == GhostState.SCATTER:
            return self._choose_scatter_direction(directions)
        if self.state == GhostState.FRIGHTENED:
            return self._choose_frightened_direction(directions)
        return self._choose_respawn_direction(directions)

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
        raise ValueError("Invalid direction.")

    def _choose_target_direction(
        self, directions: list[Direction], target_x: int, target_y: int
    ) -> Direction:
        """Choose the direction that gets closest to the target."""
        best_directions = []
        best_distance = float("inf")
        for direction in directions:
            next_x, next_y = self._next_position(direction)
            distance = abs(target_x - next_x) + abs(target_y - next_y)
            if distance < best_distance:
                best_distance = distance
                best_directions = [direction]
            elif distance == best_distance:
                best_directions.append(direction)
        return random.choice(best_directions)

    def _choose_chase_direction(
        self, directions: list[Direction], player: Player
    ) -> Direction:
        """Choose the direction that gets closest to the player."""
        target_x, target_y = self._target_position(player)
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
        self, directions: list[Direction]
    ) -> Direction:
        """Choose the direction that gets closest to the spawn."""
        return self._choose_target_direction(
            directions, self.spawn_x, self.spawn_y
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
        raise ValueError("Invalid direction.")

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

    def _target_position(self,
                         player: Player) -> tuple[int, int]:
        """Return the target position."""
        if self.state == GhostState.SCATTER:
            return self.spawn_x, self.spawn_y
        if self.ghost_type == GhostType.BLINKY:
            return player.x, player.y
        if self.ghost_type == GhostType.PINKY:
            return player.x + 2, player.y
        if self.ghost_type == GhostType.INKY:
            return player.x, player.y + 2
        return player.x - 2, player.y
