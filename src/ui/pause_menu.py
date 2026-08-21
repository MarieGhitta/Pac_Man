import pygame

from src.ui.screen import Screen


class PauseMenu(Screen):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super().__init__(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    self.next_screen = "game"

    def update(self, current_time: int) -> None:
        return super().update(current_time)

    def draw(self, surface: pygame.surface.Surface) -> None:
        pass
