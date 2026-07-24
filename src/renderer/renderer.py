"""Render the game."""

import pygame
from src.game.game import Game
from src.game.level import Level

_TILE_SIZE = 42


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
        pygame.init()
        width = level.maze.width * _TILE_SIZE
        height = level.maze.height * _TILE_SIZE
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-Man")

    def draw(self, game: Game) -> None:
        """Draw the current game state."""
        self.screen.fill((0, 0, 0))
        pygame.display.flip()