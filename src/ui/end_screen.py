import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class EndScreen(Screen):
    def __init__(
            self, surface: pygame.surface.Surface, current_time: int
    ) -> None:
        super().__init__(surface)
        self.title_font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/OptimusPrinceps.ttf", self.height // 8
        )
        self.overlay: pygame.surface.Surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.fade_start: int = current_time
        self.overlay_alpha: int = 0
        self.logo_alpha: int = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_ESCAPE:
                    self.next_screen = "quit"

    def update(self, current_time: int) -> None:
        elapsed = current_time - self.fade_start
        self.overlay_alpha = int(min(1.0, elapsed / 1500) * 255)
        if elapsed < 2500:
            logo_progress = max(0.0, (elapsed - 1000) / 1000)
            self.logo_alpha = int(min(1.0, logo_progress) * 255)
        else:
            fade_out_progress = min(1.0, (elapsed - 3500) / 800)
            self.logo_alpha = int((1.0 - fade_out_progress) * 255)

    def draw(self) -> None:
        self.overlay.fill((0, 0, 0, self.overlay_alpha))
        self.surface.blit(self.overlay, (0, 0))
        self._draw_logo(
            "YOU DIED",
            self.title_font,
            Color.RED,
            (2, 2),
            self.logo_alpha
        )
