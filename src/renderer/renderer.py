"""Render the game."""

import pygame
from src.game.game import Game
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze, Cell
from src.game.cell_content import CellContent
from src.game.ghost import Ghost
from src.game.ghost_type import GhostType
from src.game.ghost_state import GhostState


_TILE_SIZE = 84
_PADDING = 80
_FONT_SIZE = 72


class Renderer:
    """Draw the game."""

    def __init__(self, level: Level) -> None:
        """Initialize the renderer."""
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
        self._draw_ghosts(game.ghosts)
        self._draw_player(game.player)
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

    def _draw_ghosts(self, ghosts: list[Ghost]) -> None:
        """Draw all ghosts."""
        for ghost in ghosts:
            self._draw_ghost(ghost)

    def _draw_ghost(self, ghost: Ghost) -> None:
        screen_x = _PADDING + ghost.x * _TILE_SIZE
        screen_y = _PADDING + ghost.y * _TILE_SIZE
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
