import pygame

from src.game.direction import Direction
from src.game.engine import Engine
from src.renderer.renderer import Renderer
from src.ui.screens.screen import Screen
from src.utils.screen_state import ScreenState


class GameScreen(Screen):
    def __init__(
        self,
        surface: pygame.surface.Surface,
        engine: Engine,
        renderer: Renderer
    ) -> None:
        super().__init__(surface)
        self.engine = engine
        self.renderer = renderer

    def handle_event(self, event: pygame.event.Event) -> None:
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
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.PAUSE
                case pygame.K_q:
                    self.next_screen = ScreenState.QUIT

    def update(self, current_time: int) -> None:
        self.engine.update()
        if self.engine.game_over or self.engine.victory:
            self.next_screen = ScreenState.END

    def draw(self) -> None:
        self.renderer.draw(self.engine)
