"""Title screen displayed at game startup."""


import pygame

from src.app import ScreenState
from src.utils.color import Color
from src.ui.screens.screen import Screen


class TitleScreen(Screen):
    """Title screen with logo, animation, and main menu."""

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the title screen.

        Args:
            surface: The pygame surface to draw onto.
        """
        super().__init__(surface)
        self.title_font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/CrackMan.ttf", self.height // 8
        )
        self.menu_items = [
            "Play", "Highscore", "Cheat Mode", "Quit"
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    match self.menu_index:
                        case 0:
                            self.next_screen = ScreenState.GAME
                        case 1:
                            self.next_screen = ScreenState.HIGHSCORE
                        case 2:
                            self.next_screen = ScreenState.CHEAT
                        case 3:
                            self.next_screen = ScreenState.QUIT
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.QUIT

    def update(self, current_time: int) -> None:
        """Advance the screen's internal state.

        Args:
            current_time: Current time in milliseconds.
        """
        pass

    def draw(self) -> None:
        """Render the screen onto the given surface."""
        self.surface.fill(Color.BLACK)
        self._draw_logo("Pac-Man", self.title_font, Color.YELLOW, (2, 4))
        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height * 3 // 4 - total_height // 2
        self._draw_menu(self.menu_items, self.font, line_height, menu_start_y)
