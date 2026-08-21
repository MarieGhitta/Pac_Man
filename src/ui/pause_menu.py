"""Pause menu screen displayed over a frozen game frame."""


import pygame

from src.ui.screen import Screen
from src.utils.color import Color


class PauseMenu(Screen):
    """In-game pause menu rendered over a frozen frame.

    Triggered by pressing ESC during gameplay. The game loop stops updating
    while this screen is active. Offers Resume, Main Menu, and Quit options.
    """

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the pause menu.

        Args:
            surface: The pygame surface to draw onto.
        """
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
                            self.next_screen = "game"
                        case 1:
                            self.next_screen = "title"
                        case 2:
                            self.next_screen = "quit"
                case pygame.K_ESCAPE:
                    self.next_screen = "game"

    def update(self, current_time: int) -> None:
        """No-op: the pause menu has no animated state.

        Args:
            current_time: Current time in milliseconds (unused).
        """
        pass

    def draw(self) -> None:
        """Render the overlay and menu items onto the surface."""
        self.surface.blit(self.overlay, (0, 0))

        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height // 2 - total_height // 3
        self._draw_menu(line_height, menu_start_y)

    def _draw_overlay(self) -> pygame.surface.Surface:
        """Create a semi-transparent black overlay covering the full surface.

        Returns:
            A pygame Surface with per-pixel alpha, filled with ALPHA_BLACK.
        """
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(Color.ALPHA_BLACK)
        return overlay
