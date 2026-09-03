"""Manage Ghost."""


import math
import random

import pygame

from src.game.level import Level
from src.game.player import Player
from src.maze.models import Cell
from src.utils.sprite_enums import GhostState, GhostType, Direction


class Ghost:
    """Represent a ghost entity with movement and state logic."""

    def __init__(
        self,
        x: int,
        y: int,
        ghost_type: GhostType,
        last_update: int,
        update_delay: int
    ) -> None:
        """Initialize the ghost at a given tile position.

        Args:
            x: Starting tile column.
            y: Starting tile row.
            ghost_type: Identity of the ghost.
            last_update: Timestamp of the last movement tick.
            update_delay: Milliseconds between movement ticks.
        """
        self.x = x
        self.y = y
        self.ghost_type = ghost_type
        self.last_update = last_update
        self.update_delay = update_delay
        self.spawn_x: int = x
        self.spawn_y: int = y
        self.direction: Direction = Direction.UP
        self.state: GhostState = GhostState.SCATTER
        self.frightened_until: int = 0
        self.prev_x: int = x
        self.prev_y: int = y

    def update(
        self,
        level: Level,
        player: Player,
        ghosts: list["Ghost"],
        current_state: GhostState
    ) -> None:
        """Advance the ghost by one tick.

        Args:
            level: Current level.
            player: Player instance.
            ghosts: All ghosts, used for Inky's targeting.
            current_state: Global Chase/Scatter state to restore to.
        """
        current_time: int = pygame.time.get_ticks()
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
        """Return the next direction based on the ghost's current state.

        Args:
            level: Current level.
            player: Player instance.
            ghosts: All ghosts, used for Inky's targeting.

        Returns:
            Chosen direction.
        """
        directions: list[Direction] = self._possible_directions(level)
        directions = self._remove_opposite_direction(directions)
        match self.state:
            case GhostState.SCATTER:
                return self._choose_scatter_direction(directions)
            case GhostState.CHASE:
                return self._choose_chase_direction(directions, player, ghosts)
            case GhostState.FRIGHTENED | GhostState.FLICKER:
                return self._choose_frightened_direction(directions)
            case GhostState.RESPAWN:
                return self._choose_respawn_direction(directions, level)

    def _possible_directions(self, level: Level) -> list[Direction]:
        """Return all directions not blocked by a wall.

        Args:
            level: Current level.

        Returns:
            List of available directions.
        """
        current_cell: Cell = level.maze.cells[self.y][self.x]
        directions: list[Direction] = []
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
        """Move the ghost one tile in its current direction if not blocked.

        Args:
            level: Current level.
        """
        current_cell: Cell = level.maze.cells[self.y][self.x]
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
        """Return the tile coordinates one step in the given direction.

        Args:
            direction: Direction to project.

        Returns:
            (x, y) of the next tile.
        """
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
        """Return the distance to the target.

        Args:
            directions: Available directions.
            target_x: Target tile column.
            target_y: Target tile row.

        Returns:
            Best direction toward the target.
        """
        best_directions: list[Direction] = []
        best_distance: float = float("inf")
        for direction in directions:
            next_x, next_y = self._next_position(direction)
            distance: float = abs(target_x - next_x) + abs(target_y - next_y)
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
        """Return the direction toward the ghost's chase target.

        Args:
            directions: Available directions.
            player: Player instance.
            ghosts: All ghosts, used for Inky's targeting.

        Returns:
            Best direction toward the chase target.
        """
        target_x, target_y = self._target_position(player, ghosts)
        return self._choose_target_direction(directions, target_x, target_y)

    def _choose_scatter_direction(
        self, directions: list[Direction]
    ) -> Direction:
        """Return the direction toward the ghost's spawn corner.

        Args:
            directions: Available directions.

        Returns:
            Best direction toward the scatter corner.
        """
        return self._choose_target_direction(
            directions, self.spawn_x, self.spawn_y
        )

    def _choose_frightened_direction(
        self, directions: list[Direction]
    ) -> Direction:
        """Return a random available direction.

        Args:
            directions: Available directions.

        Returns:
            Randomly chosen direction.
        """
        return random.choice(directions)

    def _choose_respawn_direction(
        self, directions: list[Direction], level: Level
    ) -> Direction:
        """Return the direction toward the level's start cell.

        Args:
            directions: Available directions.
            level: Current level.

        Returns:
            Best direction toward the spawn point.
        """
        return self._choose_target_direction(
            directions, level.start_cell.x, level.start_cell.y
        )

    def _opposite_direction(self) -> Direction:
        """Return the direction opposite to the ghost's current direction.

        Returns:
            Opposite direction.
        """
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
        """Remove the opposite direction unless it is the only option.

        Args:
            directions: Available directions.

        Returns:
            Filtered list of directions.
        """
        remaining_directions: list[Direction] = []
        if len(directions) == 1:
            return directions
        opposite: Direction = self._opposite_direction()
        for direction in directions:
            if direction != opposite:
                remaining_directions.append(direction)
        return remaining_directions

    def _target_position(
        self, player: Player, ghosts: list["Ghost"]
    ) -> tuple[int, int]:
        """Return the chase target tile for this ghost type.

        Args:
            player: Player instance.
            ghosts: All ghosts, used for Inky's targeting.

        Returns:
            (x, y) of the target tile.
        """
        match self.ghost_type:
            case GhostType.BLINKY:
                return player.x, player.y
            case GhostType.PINKY:
                return self._position_ahead(player, 4)
            case GhostType.INKY:
                pivot: tuple[int, int] = self._position_ahead(player, 2)
                blinky: Ghost = next(
                    g for g in ghosts if g.ghost_type == GhostType.BLINKY
                )
                return pivot[0] * 2 - blinky.x, pivot[1] * 2 - blinky.y
            case GhostType.CLYDE:
                if math.hypot(self.x - player.x, self.y - player.y) >= 8:
                    return player.x, player.y
                else:
                    return self.spawn_x, self.spawn_y

    def _position_ahead(self, player: Player, n: int) -> tuple[int, int]:
        """Return the tile n steps ahead of the player, with UP overflow.

        Args:
            player: Player instance.
            n: Number of tiles ahead.

        Returns:
            (x, y) of the projected tile.
        """
        match player.direction:
            case Direction.UP:
                return player.x - n, player.y - n
            case Direction.DOWN:
                return player.x, player.y + n
            case Direction.LEFT:
                return player.x - n, player.y
            case Direction.RIGHT:
                return player.x + n, player.y
