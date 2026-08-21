import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class PauseMenu(Screen):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super().__init__(surface)
        self.overlay = self._draw_overlay()
        self.font_size = self.height // 16
        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )
        self.menu_items = [
            "Resume", "Main Menu", "Quit"
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    match self.menu_index:
                        case 0:
                            self.next_screen = "game"
                        case 1:
                            self.next_screen = "title"
                        case 2:
                            self.next_screen = "quit"
                case pygame.K_ESCAPE:
                    self.next_screen = "game"

    def update(self, current_time: int) -> None:
        return super().update(current_time)

    def draw(self) -> None:
        self.surface.blit(self.overlay, (0, 0))

        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height // 2 - total_height // 3
        self._draw_menu(line_height, menu_start_y)

    def _draw_overlay(self) -> pygame.surface.Surface:
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(Color.ALPHA_BLACK)
        return overlay
