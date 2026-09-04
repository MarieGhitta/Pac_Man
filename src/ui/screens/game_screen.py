"""Delegate input, update and rendering to Engine and Renderer."""


import pygame

from src.game.engine import Engine
from src.renderer.renderer import Renderer
from src.ui.screens.screen import Screen
from src.utils.screen_state import ScreenState
from src.utils.sprite_enums import Direction


class GameScreen(Screen):
    """Screen active during gameplay."""

    def __init__(
        self,
        surface: pygame.surface.Surface,
        engine: Engine,
        renderer: Renderer
    ) -> None:
        """Initialize the game screen.

        Args:
            surface: The pygame surface to draw onto.
            engine: The game engine managing game state.
            renderer: The renderer responsible for drawing the game.
        """
        super().__init__(surface)
        self.engine = engine
        self.renderer = renderer

    def handle_event(self, event: pygame.event.Event) -> None:
        """Forward direction keys to the player and handle pause/quit.

        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    self.engine.player.next_direction = Direction.UP
                case pygame.K_RIGHT:
                    self.engine.player.next_direction = Direction.RIGHT
                case pygame.K_DOWN:
                    self.engine.player.next_direction = Direction.DOWN
                case pygame.K_LEFT:
                    self.engine.player.next_direction = Direction.LEFT
                case pygame.K_ESCAPE | pygame.K_p:
                    self.next_screen = ScreenState.PAUSE
                case pygame.K_q:
                    self.next_screen = ScreenState.QUIT

    def update(self, current_time: int) -> None:
        """Advance the engine and emit END on game over or victory.

        Args:
            current_time: Current time in milliseconds.
        """
        del current_time
        self.engine.update()
        if self.engine.game_over or self.engine.victory:
            self.next_screen = ScreenState.END

    def draw(self) -> None:
        """Delegate rendering to the renderer."""
        self.renderer.draw(self.engine)
