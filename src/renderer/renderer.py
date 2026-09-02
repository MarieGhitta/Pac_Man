"""Render the game."""


import pygame

from src.game.cell_content import CellContent
from src.game.engine import Engine
from src.game.ghost import Ghost
from src.game.level import Level
from src.game.player import Player
from src.maze.models import Maze, Cell
from src.renderer.sprite import PacmanSprite, GhostSprite
from src.utils.color import Color
from src.utils.sprite_enums import GhostState, GhostType, PacmanState


class Renderer:
    """Draw the game."""

    def __init__(
        self,
        level: Level,
        surface: pygame.surface.Surface,
        highscore: int
    ) -> None:
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
        self.highscore = str(highscore)[:7]
        self.tile_size: int = min(
            int(self.surface_width * 0.80) // (self.maze_width + 1),
            int(self.surface_height * 0.70) // (self.maze_height + 1)
        )
        self.maze_offset: int = self.tile_size // 2
        self.logical_surface = pygame.Surface((
            (self.maze_width + 1) * self.tile_size,
            (self.maze_height + 1) * self.tile_size
        ))
        self.scaled_w: int = (self.maze_width + 1) * self.tile_size
        self.scaled_h: int = (self.maze_height + 1) * self.tile_size
        self.offset_x: int = (self.surface_width - self.scaled_w) // 2
        self.offset_y: int = (self.surface_height - self.scaled_h) // 2
        self.maze_offset: int = self.tile_size // 2
        self.font_size: int = self.surface_height // 48
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )
        self.countdown_font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size * 7
        )
        self.pacman_sprite: PacmanSprite = PacmanSprite(self.tile_size)
        self.ghost_sprites = {
            GhostType.BLINKY: GhostSprite(self.tile_size, Color.RED),
            GhostType.PINKY: GhostSprite(self.tile_size, Color.PINK),
            GhostType.INKY: GhostSprite(self.tile_size, Color.CYAN),
            GhostType.CLYDE: GhostSprite(self.tile_size, Color.ORANGE)
        }

    def draw(self, game: Engine) -> None:
        """Draw the current game state: maze, player, ghosts, and HUD.

        Args:
            game: The current game state.
        """
        self.surface.fill(Color.BLACK)
        dying = game.dying or (game.game_over and not game.victory)
        self._update_window(game.level)
        self.logical_surface.fill(Color.BLACK)
        current_time = pygame.time.get_ticks()
        self._draw_maze(game.level.maze, current_time)
        if not dying:
            self._draw_ghosts(game.ghosts, current_time)
        self._draw_player(game.player, current_time, dying)
        # scaled = pygame.transform.scale(
        #     self.logical_surface, (self.scaled_w, self.scaled_h)
        # )
        self.surface.blit(self.logical_surface, (self.offset_x, self.offset_y))
        self._draw_hud(game, current_time)
        if game.counting_down:
            self._draw_countdown(game.countdown)

    def _draw_maze(self, maze: Maze, current_time: int) -> None:
        """Draw all maze cells, including walls and cell contents.

        Args:
            maze: The maze to draw.
        """
        for row in maze.cells:
            for cell in row:
                surface_x = cell.x * self.tile_size + self.maze_offset
                surface_y = cell.y * self.tile_size + self.maze_offset
                self._draw_walls(cell, surface_x, surface_y)
                self._draw_cell_content(cell, current_time)

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
        """Draw a wall segment as a blue tube: thick blue line with a black
        inner line to create a hollow outlined effect.

        Args:
            start_pos: Screen coordinates of the wall's start point.
            end_pos: Screen coordinates of the wall's end point.
        """
        pygame.draw.line(
            self.logical_surface, Color.BLUE, start_pos, end_pos,
            max(1, self.tile_size // 8)
        )

    def _draw_cell_content(self, cell: Cell, current_time: int) -> None:
        """Draw the content of a maze cell.

        Args:
            cell: The maze cell whose content is drawn.
        """
        center_x, center_y = self._to_screen(cell.x, cell.y, centered=True)
        match cell.content:
            case CellContent.PACGUM:
                pygame.draw.rect(
                    self.logical_surface,
                    Color.LIGHTPINK,
                    (
                        center_x - self.tile_size // 12,
                        center_y - self.tile_size // 12,
                        self.tile_size // 6,
                        self.tile_size // 6
                    )
                )
            case CellContent.SUPER_PACGUM:
                if (current_time // 150) % 2 == 0:
                    pygame.draw.circle(
                        self.logical_surface,
                        Color.LIGHTPINK,
                        (center_x, center_y),
                        self.tile_size // 4,
                    )

    def _draw_player(
        self, player: Player, current_time: int, dying: bool
    ) -> None:
        """Draw the player at its interpolated position.

        Args:
            player: The player to draw.
            current_time: Current time in milliseconds for interpolation.
        """
        render_x, render_y = self._interpolate(player, current_time)
        center_x, center_y = self._to_screen(render_x, render_y)
        variant = (
            (None, PacmanState.DYING)
            if dying else (player.direction, PacmanState.ALIVE)
        )
        self.pacman_sprite.update(current_time, variant)
        self.pacman_sprite.draw(
            self.logical_surface, center_x, center_y, variant
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
            round(x * self.tile_size + half + self.maze_offset + 1),
            round(y * self.tile_size + half + self.maze_offset + 1)
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

    def _draw_hud(self, game: Engine, current_time: int) -> None:
        """Draw the HUD: score on the left, lives on the right.

        Args:
            game: The current game state.
            current_time: the current time in milliseconds.
        """
        line_height = int(self.font.get_height() * 1.2)
        self._draw_text(
            "1UP",
            self.surface_width // 3,
            self.surface_height // 8,
            Color.WHITE,
            current_time,
            True
        )
        self._draw_text(
            str(game.score),
            self.surface_width // 3,
            self.surface_height // 8 + line_height
        )
        self._draw_text(
            "HIGH SCORE",
            self.surface_width // 2,
            self.surface_height // 8
        )
        self._draw_text(
            self.highscore,
            self.surface_width // 2,
            self.surface_height // 8 + line_height
        )
        self._draw_text(
            "TIME",
            self.surface_width - (self.surface_width // 3),
            self.surface_height // 8
        )
        self._draw_text(
            str(game.time_remaining),
            self.surface_width - (self.surface_width // 3),
            self.surface_height // 8 + line_height
        )
        self._draw_text(
            "LEVEL",
            self.surface_width - (self.surface_width // 3),
            self.surface_height * 7 // 8 - line_height
        )
        self._draw_text(
            f"{str(game.current_level_index + 1)}/{game.max_level_index}",
            self.surface_width - (self.surface_width // 3),
            self.surface_height * 7 // 8
        )
        if self.pacman_sprite.life is not None:
            life_sprite = pygame.transform.scale(
                self.pacman_sprite.life,
                (self.font_size * 2.2, self.font_size * 2.2)
            )
            if game.lives < 10:
                sprite_offset = 0.0
                for _ in range(game.lives):
                    self._draw_life_sprite(
                        life_sprite, line_height, sprite_offset
                    )
                    sprite_offset += self.font_size * 1.8
            else:
                self._draw_life_sprite(life_sprite, line_height)
                self._draw_text(
                    f"x{str(game.lives)}",
                    self.surface_width // 3 + life_sprite.get_width() + line_height // 4,
                    self.surface_height * 7 // 8 - line_height
                )

    def _draw_life_sprite(
        self,
        life_sprite: pygame.surface.Surface,
        line_height: int,
        offset: float = 0.0
    ) -> None:
        self.surface.blit(
            life_sprite,
            (
                self.surface_width // 3 - line_height + offset,
                self.surface_height - (self.surface_height // 6),
            )
        )

    def _draw_text(
        self,
        text: str,
        x: int,
        y: int,
        color: tuple[int, int, int] = Color.WHITE,
        current_time: int = 0,
        blink: bool = False,
    ) -> None:
        display = self.font.render(text, True, color)
        display_rect = display.get_rect(center=(x, y))
        if blink:
            if (current_time // 250) % 2 == 0:
                self.surface.blit(display, display_rect)
        else:
            self.surface.blit(display, display_rect)

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
            int(self.surface_width * 0.80) // (self.maze_width + 1),
            int(self.surface_height * 0.70) // (self.maze_height + 1)
        )
        self.maze_offset = self.tile_size // 2
        self.logical_surface = pygame.Surface((
            (self.maze_width + 1) * self.tile_size,
            (self.maze_height + 1) * self.tile_size
        ))
        self.scaled_w = (self.maze_width + 1) * self.tile_size
        self.scaled_h = (self.maze_height + 1) * self.tile_size
        self.offset_x = (self.surface_width - self.scaled_w) // 2
        self.offset_y = (self.surface_height - self.scaled_h) // 2
        self.pacman_sprite = PacmanSprite(self.tile_size)
        self.ghost_sprites = {
            GhostType.BLINKY: GhostSprite(self.tile_size, Color.RED),
            GhostType.PINKY: GhostSprite(self.tile_size, Color.PINK),
            GhostType.INKY: GhostSprite(self.tile_size, Color.CYAN),
            GhostType.CLYDE: GhostSprite(self.tile_size, Color.ORANGE)
        }

    def _draw_ghosts(self, ghosts: list[Ghost], current_time: int) -> None:
        """Draw all ghosts.

        Args:
            ghosts: List of ghosts to draw.
            current_time: Current time in milliseconds for interpolation.
        """
        for ghost in ghosts:
            render_x, render_y = self._interpolate(ghost, current_time)
            corner_x, corner_y = self._to_screen(render_x, render_y)
            visual_state = self._visual_ghost_state(ghost, current_time)
            sprite = self.ghost_sprites[ghost.ghost_type]
            sprite.update(
                current_time,
                (ghost.direction, visual_state)
            )
            sprite.draw(
                self.logical_surface,
                corner_x,
                corner_y,
                (ghost.direction, visual_state)
            )

    def _visual_ghost_state(
        self, ghost: Ghost, current_time: int
    ) -> GhostState:
        if (
            ghost.state == GhostState.FRIGHTENED
            and ghost.frightened_until - current_time <= 2000
        ):
            if (current_time // 250) % 2 == 0:
                return GhostState.FLICKER
        return ghost.state

    def _draw_countdown(self, countdown: int) -> None:
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.surface.blit(overlay, (0, 0))
        text = self.countdown_font.render(str(countdown), True, Color.YELLOW)
        rect = text.get_rect(center=(
            self.surface.get_width() // 2, self.surface.get_height() // 2)
        )
        self.surface.blit(text, rect)
