import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class EndScreen(Screen):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super().__init__(surface)
        self.title_font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/OptimusPrinceps.ttf", self.height // 8
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        return super().handle_event(event)

    def update(self, current_time: int) -> None:
        return super().update(current_time)

    def draw(self) -> None:
        self.surface.fill(Color.BLACK)
        self._draw_logo("YOU DIED", self.title_font, Color.RED, (2, 2))
