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


_TILE_SIZE = 84
_PADDING = 80
_FONT_SIZE = 72


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
        # window_width = level.maze.width * _TILE_SIZE + 2 * _PADDING
        # window_height = level.maze.height * _TILE_SIZE + 2 * _PADDING
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        self.offset_x = (
            (self.screen_width - self.maze_width * _TILE_SIZE) // 2
        )
        self.offset_y = (
            (self.screen_height - self.maze_height * _TILE_SIZE) // 2
        )
        pygame.display.set_caption("Pac-Man")
        self.font = pygame.font.Font(None, _FONT_SIZE)

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
        self._draw_score(game)
        pygame.display.flip()

    def _draw_maze(self, maze: Maze) -> None:
        """Draw the maze."""
        for row in maze.cells:
            for cell in row:
                screen_x = _PADDING + cell.x * _TILE_SIZE
                screen_y = _PADDING + cell.y * _TILE_SIZE
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
                (screen_x + _TILE_SIZE, screen_y)
            )
        if cell.east_wall:
            self._draw_wall(
                (screen_x + _TILE_SIZE, screen_y),
                (screen_x + _TILE_SIZE, screen_y + _TILE_SIZE) 
            )
        if cell.south_wall:
            self._draw_wall(
                (screen_x, screen_y + _TILE_SIZE),
                (screen_x + _TILE_SIZE, screen_y + _TILE_SIZE),
            )
        if cell.west_wall:
            self._draw_wall(
                (screen_x, screen_y),
                (screen_x, screen_y + _TILE_SIZE),
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

    def _draw_cell_content(self, cell: Cell,
                           screen_x: int, screen_y: int) -> None:
        """Draw the content of a maze cell."""
        center = (screen_x + _TILE_SIZE // 2,
                  screen_y + _TILE_SIZE // 2)
        if cell.content == CellContent.PACGUM:
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                center,
                _TILE_SIZE // 8,
            )
        elif cell.content == CellContent.SUPER_PACGUM:
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                center,
                _TILE_SIZE // 4,
            )

    def _draw_player(self, player: Player, alpha: float) -> None:
        """Draw the player.

        Args:
            player: The player to draw.
            alpha: Interpolation factor between previous and current position.
        """
        render_x = player.prev_x + (player.x - player.prev_x) * alpha
        render_y = player.prev_y + (player.y - player.prev_y) * alpha
        center_x = int(_PADDING + render_x * _TILE_SIZE + _TILE_SIZE // 2)
        center_y = int(_PADDING + render_y * _TILE_SIZE + _TILE_SIZE // 2)
        pygame.draw.circle(
            self.screen,
            (255, 255, 0),
            (center_x, center_y),
            _TILE_SIZE // 3,
        )

    def _draw_score(self, game: Game) -> None:
        """Draw the current score."""
        score_text = self.font.render(
            f'Score: {game.score}',
            True,
            (255, 255, 255)
        )
        self.screen.blit(score_text, (_PADDING, 10))
        lives_text = self.font.render(
            f"Lives: {game.lives}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(lives_text, (self.screen.get_width() -
                                      lives_text.get_width() - _PADDING, 10))

    def _update_window(self, level: Level) -> None:
        """Resize the window if the level dimensions changed."""
        if (level.maze.width == self.maze_width
           and level.maze.height == self.maze_height):
            return
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height
        width = self.maze_width * _TILE_SIZE + 2 * _PADDING
        height = self.maze_height * _TILE_SIZE + 2 * _PADDING
        self.screen = pygame.display.set_mode((width, height))

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
        screen_x = int(_PADDING + render_x * _TILE_SIZE)
        screen_y = int(_PADDING + render_y * _TILE_SIZE)
        margin = _TILE_SIZE // 4
        points = [
            (screen_x + _TILE_SIZE // 2, screen_y + margin),
            (screen_x + _TILE_SIZE - margin, screen_y + _TILE_SIZE - margin),
            (screen_x + margin, screen_y + _TILE_SIZE - margin)
        ]
        pygame.draw.polygon(self.screen, self._ghost_color(ghost), points)

    def _ghost_color(self, ghost: Ghost) -> tuple[int, int, int]:
        """Return the ghost color."""
        if ghost.state == GhostState.FRIGHTENED:
            return (0, 0, 255)
        if ghost.state == GhostState.RESPAWN:
            return (255, 255, 255)
        if ghost.ghost_type == GhostType.BLINKY:
            return (255, 0, 0)
        if ghost.ghost_type == GhostType.PINKY:
            return (255, 105, 180)
        if ghost.ghost_type == GhostType.INKY:
            return (0, 255, 255)
        if ghost.ghost_type == GhostType.CLYDE:
            return (255, 128, 0)
        raise ValueError(f"unknown ghost type: {ghost.ghost_type}")
