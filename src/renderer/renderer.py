"""Render the game."""


import pygame

from src.game.cell_content import CellContent
from src.game.engine import Engine
from src.game.ghost import Ghost
from src.game.ghost_type import GhostType
from src.game.ghost_state import GhostState
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze, Cell
from src.utils.color import Color


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level, surface: pygame.surface.Surface) -> None:
        """Initialize the renderer and create the fullscreen window.

        Args:
            level: The initial game level.
            surface: The pygame surface to draw onto.
        """
        self.surface = surface
        self.surface_width = surface.get_width()
        self.surface_height = surface.get_height()
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        self.tile_size: int = min(
            int(self.surface_width * 0.8) // self.maze_width,
            int(self.surface_height * 0.8) // self.maze_height
        )
        self.offset_x = (
            (self.surface_width - self.maze_width * self.tile_size) // 2
        )
        self.offset_y = (
            (self.surface_height - self.maze_height * self.tile_size) // 2
        )
        self.font = pygame.font.Font(None, self.tile_size)

    def draw(self, game: Engine) -> None:
        """Draw the current game state: maze, player, ghosts, and HUD.

        Args:
            game: The current game state.
        """
        self._update_window(game.level)
        self.surface.fill(Color.BLACK)
        self._draw_maze(game.level.maze)
        current_time = pygame.time.get_ticks()
        self._draw_player(game.player, current_time)
        self._draw_ghosts(game.ghosts, current_time)
        self._draw_hud(game)

    def _draw_maze(self, maze: Maze) -> None:
        """Draw all maze cells, including walls and cell contents.

        Args:
            maze: The maze to draw.
        """
        for row in maze.cells:
            for cell in row:
                surface_x = self.offset_x + cell.x * self.tile_size
                surface_y = self.offset_y + cell.y * self.tile_size
                self._draw_walls(cell, surface_x, surface_y)
                self._draw_cell_content(cell)

    def _draw_walls(self, cell: Cell, x: int, y: int) -> None:
        """Draw the walls of a maze cell.

        Args:
            cell: The maze cell whose walls are drawn.
            x: Pixel x-coordinate of the cell's top-left corner.
            y: Pixel y-coordinate of the cell's top-left corner.
        """
        if cell.north_wall:
            self._draw_wall(
                (x, y),
                (x + self.tile_size, y)
            )
        if cell.east_wall:
            self._draw_wall(
                (x + self.tile_size, y),
                (x + self.tile_size, y + self.tile_size)
            )
        if cell.south_wall:
            self._draw_wall(
                (x, y + self.tile_size),
                (x + self.tile_size, y + self.tile_size),
            )
        if cell.west_wall:
            self._draw_wall(
                (x, y),
                (x, y + self.tile_size),
            )

    def _draw_wall(
        self, start_pos: tuple[int, int], end_pos: tuple[int, int]
    ) -> None:
        """Draw a single wall segment as a blue line.

        Args:
            start_pos: Screen coordinates of the wall's start point.
            end_pos: Screen coordinates of the wall's end point.
        """
        pygame.draw.line(self.surface, Color.BLUE, start_pos, end_pos, 3)

    def _draw_cell_content(self, cell: Cell) -> None:
        """Draw the content of a maze cell.

        Args:
            cell: The maze cell whose content is drawn.
        """
        center_x, center_y = self._to_screen(cell.x, cell.y, centered=True)
        match cell.content:
            case CellContent.PACGUM:
                pygame.draw.circle(
                    self.surface,
                    Color.WHITE,
                    (center_x, center_y),
                    self.tile_size // 8,
                )
            case CellContent.SUPER_PACGUM:
                pygame.draw.circle(
                    self.surface,
                    Color.WHITE,
                    (center_x, center_y),
                    self.tile_size // 4,
                )

    def _draw_player(self, player: Player, current_time: int) -> None:
        """Draw the player at its interpolated position.

        Args:
            player: The player to draw.
            current_time: Current time in milliseconds for interpolation.
        """
        render_x, render_y = self._interpolate(player, current_time)
        center_x, center_y = self._to_screen(render_x, render_y, centered=True)
        pygame.draw.circle(
            self.surface,
            Color.YELLOW,
            (center_x, center_y),
            self.tile_size // 3,
        )

    def _to_screen(
        self, x: float, y: float, centered: bool = False
    ) -> tuple[int, int]:
        """Convert grid coordinates to screen pixel coordinates.

        Args:
            x: Horizontal grid coordinate.
            y: Vertical grid coordinate.
            centered: If True, offset by half a tile to target the tile center.

        Returns:
            Pixel coordinates on screen.
        """
        half = self.tile_size // 2 if centered else 0
        return (
            int(self.offset_x + x * self.tile_size + half),
            int(self.offset_y + y * self.tile_size + half)
        )

    def _interpolate(
        self, sprite: Player | Ghost, current_time: int
    ) -> tuple[float, float]:
        """Compute the interpolated grid position of a sprite.

        Args:
            sprite: The player or ghost to interpolate.
            current_time: Current time in milliseconds.

        Returns:
            Interpolated (x, y) grid coordinates as floats.
        """
        alpha = min(
            1.0, (current_time - sprite.last_update) / sprite.update_delay
        )
        return (
            sprite.prev_x + (sprite.x - sprite.prev_x) * alpha,
            sprite.prev_y + (sprite.y - sprite.prev_y) * alpha
        )

    def _draw_hud(self, game: Engine) -> None:
        """Draw the HUD: score on the left, lives on the right.

        Args:
            game: The current game state.
        """
        score_txt = self.font.render(
            f'Score: {game.score}',
            True,
            Color.WHITE
        )
        lives_txt = self.font.render(
            f"Lives: {game.lives}",
            True,
            Color.WHITE
        )
        self.surface.blit(
            score_txt,
            (self.offset_x, self.offset_y - self.tile_size)
        )
        self.surface.blit(
            lives_txt,
            (
                self.surface_width - lives_txt.get_width() - self.offset_x,
                self.offset_y - self.tile_size
            )
        )

    def _update_window(self, level: Level) -> None:
        """Recalculate offsets if the level dimensions changed.

        Args:
            level: The current game level.
        """
        if (
            level.maze.width == self.maze_width
            and level.maze.height == self.maze_height
        ):
            return
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        self.tile_size = min(
            int(self.surface_width * 0.8) // self.maze_width,
            int(self.surface_height * 0.8) // self.maze_height
        )
        self.offset_x = (
            (self.surface_width - self.maze_width * self.tile_size) // 2
        )
        self.offset_y = (
            (self.surface_height - self.maze_height * self.tile_size) // 2
        )

    def _draw_ghosts(self, ghosts: list[Ghost], current_time: int) -> None:
        """Draw all ghosts.

        Args:
            ghosts: List of ghosts to draw.
            current_time: Current time in milliseconds for interpolation.
        """
        for ghost in ghosts:
            render_x, render_y = self._interpolate(ghost, current_time)
            corner_x, corner_y = self._to_screen(render_x, render_y)
            margin = self.tile_size // 4
            points = [
                (corner_x + self.tile_size // 2, corner_y + margin),
                (
                    corner_x + self.tile_size - margin,
                    corner_y + self.tile_size - margin
                ),
                (corner_x + margin, corner_y + self.tile_size - margin)
            ]
            pygame.draw.polygon(self.surface, self._ghost_color(ghost), points)

    def _ghost_color(self, ghost: Ghost) -> tuple[int, int, int]:
        """Return the display color of a ghost based on its state and type.

        Args:
            ghost: The ghost whose color is determined.

        Returns:
            RGB color tuple.
        """
        match ghost.state:
            case GhostState.FRIGHTENED:
                return Color.BLUE
            case GhostState.RESPAWN:
                return Color.WHITE

        match ghost.ghost_type:
            case GhostType.BLINKY:
                return Color.RED
            case GhostType.PINKY:
                return Color.PINK
            case GhostType.INKY:
                return Color.CYAN
            case GhostType.CLYDE:
                return Color.ORANGE
