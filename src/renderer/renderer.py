"""Render the game."""


import pygame

from src.game.cell_content import CellContent
from src.game.game import Game
from src.game.ghost import Ghost
from src.game.ghost_type import GhostType
from src.game.ghost_state import GhostState
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze, Cell


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN | pygame.SCALED
        )
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        self.tile_size = min(
            int(self.screen_width * 0.8) // self.maze_width,
            int(self.screen_height * 0.8) // self.maze_height
        )
        self.offset_x = (self.screen_width - self.maze_width * self.tile_size) // 2
        self.offset_y = (self.screen_height - self.maze_height * self.tile_size) // 2
        pygame.display.set_caption("Pac-Man")
        self.font = pygame.font.Font(None, self.tile_size)

    def draw(self, game: Game) -> None:
        """Draw the current game state."""
        self._update_window(game.level)
        self.screen.fill((0, 0, 0))
        self._draw_maze(game.level.maze)
        current_time = pygame.time.get_ticks()
        player_alpha = min(
            1.0,
            (current_time - game.last_player_update) / game.player_update_delay
        )
        self._draw_player(game.player, player_alpha)
        self._draw_ghosts(game.ghosts, current_time)
        self._draw_hud(game)
        pygame.display.flip()

    def _draw_maze(self, maze: Maze) -> None:
        """Draw the maze."""
        for row in maze.cells:
            for cell in row:
                screen_x = self.offset_x + cell.x * self.tile_size
                screen_y = self.offset_y + cell.y * self.tile_size
                self._draw_walls(cell, screen_x, screen_y)
                self._draw_cell_content(cell, screen_x, screen_y)

    def _draw_walls(self, cell: Cell, screen_x: int, screen_y: int) -> None:
        """Draw the walls of a maze cell.

        Args:
            cell: The maze cell whose walls are drawn.
            screen_x: Pixel x-coordinate of the cell's top-left corner.
            screen_y: Pixel y-coordinate of the cell's top-left corner.
        """
        if cell.north_wall:
            self._draw_wall(
                (screen_x, screen_y),
                (screen_x + self.tile_size, screen_y)
            )
        if cell.east_wall:
            self._draw_wall(
                (screen_x + self.tile_size, screen_y),
                (screen_x + self.tile_size, screen_y + self.tile_size)
            )
        if cell.south_wall:
            self._draw_wall(
                (screen_x, screen_y + self.tile_size),
                (screen_x + self.tile_size, screen_y + self.tile_size),
            )
        if cell.west_wall:
            self._draw_wall(
                (screen_x, screen_y),
                (screen_x, screen_y + self.tile_size),
            )

    def _draw_wall(
        self, start_pos: tuple[int, int], end_pos: tuple[int, int]
    ) -> None:
        """Draw a single wall segment as a blue line.

        Args:
            start_pos: Screen coordinates of the wall's start point.
            end_pos: Screen coordinates of the wall's end point.
        """
        pygame.draw.line(self.screen, (0, 0, 255), start_pos, end_pos, 3)

    def _draw_cell_content(
        self, cell: Cell, screen_x: int, screen_y: int
    ) -> None:
        """Draw the content of a maze cell.

        Args:
            cell: The maze cell whose content is drawn.
            screen_x: Pixel x-coordinate of the cell's top-left corner.
            screen_y: Pixel y-coordinate of the cell's top-left corner.
        """
        center = (screen_x + self.tile_size // 2, screen_y + self.tile_size // 2)
        match cell.content:
            case CellContent.PACGUM:
                self._draw_circle(center, 8)
            case CellContent.SUPER_PACGUM:
                self._draw_circle(center, 4)

    def _draw_circle(self, center: tuple[int, int], size: int) -> None:
        """Draw a white filled circle on the screen.

        Args:
            center: Pixel coordinates of the circle's center.
            size: Divisor applied to self.tile_size to compute the radius.
        """
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            center,
            self.tile_size // size,
        )

    def _draw_player(self, player: Player, alpha: float) -> None:
        """Draw the player.

        Args:
            player: The player to draw.
            alpha: Interpolation factor between previous and current position.
        """
        render_x = player.prev_x + (player.x - player.prev_x) * alpha
        render_y = player.prev_y + (player.y - player.prev_y) * alpha
        center_x = int(self.offset_x + render_x * self.tile_size + self.tile_size // 2)
        center_y = int(self.offset_y + render_y * self.tile_size + self.tile_size // 2)
        pygame.draw.circle(
            self.screen,
            (255, 255, 0),
            (center_x, center_y),
            self.tile_size // 3,
        )

    def _draw_hud(self, game: Game) -> None:
        """Draw the current score."""
        score_text = self.font.render(
            f'Score: {game.score}',
            True,
            (255, 255, 255)
        )
        lives_text = self.font.render(
            f"Lives: {game.lives}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(
            score_text,
            (self.offset_x, self.offset_y - self.tile_size)
        )
        self.screen.blit(
            lives_text,
            (
                self.screen_width - lives_text.get_width() - self.offset_x,
                self.offset_y - self.tile_size
            )
        )

    def _update_window(self, level: Level) -> None:
        """Resize the window if the level dimensions changed."""
        if (
            level.maze.width == self.maze_width
            and level.maze.height == self.maze_height
        ):
            return
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        self.offset_x = (self.screen_width - self.maze_width * self.tile_size) // 2
        self.offset_y = (self.screen_height - self.maze_height * self.tile_size) // 2


    def _draw_ghosts(self, ghosts: list[Ghost], current_time: int) -> None:
        """Draw all ghosts."""
        for ghost in ghosts:
            self._draw_ghost(ghost, current_time)

    def _draw_ghost(self, ghost: Ghost, current_time: int) -> None:
        """Draw a ghost.

        Args:
            ghost: The ghost to draw.
            current_time: Current time in milliseconds for alpha computation.
        """
        alpha = min(
            1.0, (current_time - ghost.last_update) / ghost.update_delay
        )
        render_x = ghost.prev_x + (ghost.x - ghost.prev_x) * alpha
        render_y = ghost.prev_y + (ghost.y - ghost.prev_y) * alpha
        screen_x = int(self.offset_x + render_x * self.tile_size)
        screen_y = int(self.offset_y + render_y * self.tile_size)
        margin = self.tile_size // 4
        points = [
            (screen_x + self.tile_size // 2, screen_y + margin),
            (screen_x + self.tile_size - margin, screen_y + self.tile_size - margin),
            (screen_x + margin, screen_y + self.tile_size - margin)
        ]
        pygame.draw.polygon(self.screen, self._ghost_color(ghost), points)

    def _ghost_color(self, ghost: Ghost) -> tuple[int, int, int]:
        """Return the ghost color."""
        match ghost.state:
            case GhostState.FRIGHTENED:
                return (0, 0, 255)
            case GhostState.RESPAWN:
                return (255, 255, 255)

        match ghost.ghost_type:
            case GhostType.BLINKY:
                return (255, 0, 0)
            case GhostType.PINKY:
                return (255, 105, 180)
            case GhostType.INKY:
                return (0, 255, 255)
            case GhostType.CLYDE:
                return (255, 128, 0)
