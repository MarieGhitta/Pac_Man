"""Instructions screen listing the game's basic rules and controls."""


import pygame

from src.ui.screens.screen import Screen
from src.utils.color import Color
from src.utils.screen_state import ScreenState


class InstructionScreen(Screen):
    """Static screen listing the game's basic rules and controls."""

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the instruction screen.

        Args:
            surface: The pygame surface to draw onto.
        """
        super().__init__(surface)
        self.font_size: int = self.height // 64
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )
        self.menu_items = [
            "Use WASD or arrow keys to navigate Pac-man.",
            "The level is completed once Pac-man ate all pacgums on screen.",
            "Super-pacgums make ghosts frightened and edible for a while.",
            "Ghosts have different chase behavior"
            + "and kills Pac-man on collision.",
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_screen = ScreenState.TITLE

    def draw(self) -> None:
        """Render the screen onto the given surface."""
        self.surface.fill(Color.BLACK)
        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height // 2 - total_height // 2
        self._draw_menu(
            self.menu_items,
            self.font,
            line_height,
            menu_start_y,
            highlight=False
        )
