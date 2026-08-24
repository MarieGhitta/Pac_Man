import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class EndScreen(Screen):
    def __init__(
            self, surface: pygame.surface.Surface, current_time: int
    ) -> None:
        super().__init__(surface)
        self.font_size: int = self.height // 32
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )
        self.title_font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/OptimusPrinceps.ttf", self.height // 8
        )
        self.overlay: pygame.surface.Surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.fade_start: int = current_time
        self.overlay_alpha: int = 0
        self.logo_alpha: int = 0
        self.menu_alpha: int = 0
        self.score_alpha: int = 0
        self.menu_items: list[str] = [
            "Retry", "Main Menu", "Quit"
        ]
        self.can_navigate: bool = False
        self.username: str = ""
        self.score_input: list[str] = [
            "Enter your name:", self.username
        ]
        self.can_write: bool = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if self.can_write:
                match event.key:
                    case pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    case pygame.K_RETURN:
                        if len(self.username) > 2:
                            self.can_write = False
                            self.can_navigate = True
                    case _:
                        if (
                            event.unicode.isalnum()
                            and len(self.username) < 10
                        ):
                            self.username += event.unicode
                if len(self.username) == 10 and self.can_write:
                    self.can_write = False
            else:
                if self.can_navigate:
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
                            self.next_screen = "quit"
                    if self.next_screen is not None:
                        self.can_navigate = False

    def update(self, current_time: int) -> None:
        elapsed = current_time - self.fade_start
        self.overlay_alpha = int(min(1.0, elapsed / 1500) * 255)
        if elapsed < 2500:
            logo_progress = max(0.0, (elapsed - 1000) / 1000)
            self.logo_alpha = int(min(1.0, logo_progress) * 255)
        else:
            fade_out_progress = min(1.0, (elapsed - 3500) / 800)
            self.logo_alpha = int((1.0 - fade_out_progress) * 255)
            if elapsed < 5000:
                score_progress = max(0.0, (elapsed - 4300) / 1000)
                self.score_alpha = int(min(1.0, score_progress) * 255)
            else:
                if not self.can_navigate:
                    self.can_write = True
                else:
                    self.can_write = False
                    self.score_alpha = 0
                    self.menu_alpha = 255


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

        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.score_input) * line_height
        menu_start_y = self.height // 2 - total_height // 2
        self.score_input[-1] = self.username
        self._draw_menu(
            self.score_input,
            self.font,
            line_height,
            menu_start_y,
            self.score_alpha
        )

        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height * 3 // 4 - total_height // 2
        self._draw_menu(
            self.menu_items,
            self.font,
            line_height,
            menu_start_y,
            self.menu_alpha
        )
