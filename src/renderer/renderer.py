"""Render the game."""

import pygame
from src.game.game import Game
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze

_TILE_SIZE = 42
_PADDING = 20


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
        pygame.init()
        width = level.maze.width * _TILE_SIZE + 2 * _PADDING
        height = level.maze.height * _TILE_SIZE + 2 * _PADDING
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-Man")

    def draw(self, game: Game) -> None:
        """Draw the current game state."""
        self.screen.fill((0, 0, 0))
        self._draw_maze(game.level.maze)
        self._draw_player(game.player)
        pygame.display.flip()

    def _draw_maze(self, maze: Maze) -> None:
        """Draw the maze."""
        for row in maze.cells:
            for cell in row:
                screen_x = _PADDING + cell.x * _TILE_SIZE
                screen_y = _PADDING + cell.y * _TILE_SIZE
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
