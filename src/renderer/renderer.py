"""Render the game."""

import pygame
from src.game.game import Game
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze, Cell
from src.game.cell_content import CellContent


_TILE_SIZE = 42
_PADDING = 40
_FONT_SIZE = 36


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
        pygame.init()
        window_width = level.maze.width * _TILE_SIZE + 2 * _PADDING
        window_height = level.maze.height * _TILE_SIZE + 2 * _PADDING
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Pac-Man")
        self.font = pygame.font.Font(None, _FONT_SIZE)
        self.maze_width = level.maze.width
        self.maze_height = level.maze.height

    def draw(self, game: Game) -> None:
        """Draw the current game state."""
        self._update_window(game.level)
        self.screen.fill((0, 0, 0))
        self._draw_maze(game.level.maze)
        self._draw_player(game.player)
        self._draw_score(game.score)
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
        """Draw the walls of a maze cell."""
        if cell.north_wall:
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                (screen_x, screen_y),
                (screen_x + _TILE_SIZE, screen_y),
                3,
            )
        if cell.east_wall:
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                (screen_x + _TILE_SIZE, screen_y),
                (screen_x + _TILE_SIZE, screen_y + _TILE_SIZE),
                3,
            )
        if cell.south_wall:
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                (screen_x, screen_y + _TILE_SIZE),
                (screen_x + _TILE_SIZE, screen_y + _TILE_SIZE),
                3,
            )
        if cell.west_wall:
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                (screen_x, screen_y),
                (screen_x, screen_y + _TILE_SIZE),
                3,
            )

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

    def _draw_player(self, player: Player) -> None:
        """Draw the player."""
        center_x = (_PADDING + player.x * _TILE_SIZE + _TILE_SIZE // 2)
        center_y = (_PADDING + player.y * _TILE_SIZE + _TILE_SIZE // 2)
        pygame.draw.circle(
            self.screen,
            (255, 255, 0),
            (center_x, center_y),
            _TILE_SIZE // 3,
        )

    def _draw_score(self, score: int) -> None:
        """Draw the current score."""
        score_text = self.font.render(
            f'Score: {score}',
            True,
            (255, 255, 255)
        )
        self.screen.blit(score_text, (_PADDING, 10))

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
