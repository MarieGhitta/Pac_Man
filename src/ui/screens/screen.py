"""Abstract base class for game screens."""


from abc import ABC, abstractmethod

import pygame

from src.utils.color import Color
from src.utils.screen_state import ScreenState


class Screen(ABC):
    """Abstract base class for all game screens.

    Each concrete screen manages its own input handling, state update,
    and rendering. Set `next_screen` to signal a transition to the manager.
    """

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the screen with no pending transition."""
        self.next_screen: ScreenState | None = None
        self.surface = surface
        self.width: int = surface.get_width()
        self.height: int = surface.get_height()
        self.menu_items: list[str] = []
        self.menu_index: int = 0
        self.font_size: int = self.height // 32
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        pass

    def _navigate(self, key: int) -> None:
        """Update menu_index based on vertical navigation keys.

        Args:
            key: The pygame key constant (K_UP or K_DOWN).
        """
        match key:
            case pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            case pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_items)

    @abstractmethod
    def update(self, current_time: int) -> None:
        """Advance the screen's internal state.

        Args:
            current_time: Current time in milliseconds.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """Render the screen onto the given surface.

        Args:
            surface: The pygame surface to draw onto.
        """
        pass

    def _draw_logo(
        self,
        text: str,
        title_font: pygame.font.Font,
        color: tuple[int, int, int] | tuple[int, int, int, int],
        pos: tuple[int, int],
        alpha: int = 255
    ) -> None:
        """Render a centered logo text at a fractional screen position.

        Args:
            text: The text to render.
            title_font: The font to use.
            color: RGB or RGBA color of the text.
            pos: Divisors (dx, dy).
            alpha: Opacity from 0 (transparent) to 255 (opaque).
        """
        logo = title_font.render(text, True, color)
        logo_rect = logo.get_rect(
            center=(self.width // pos[0], self.height // pos[1])
        )
        logo.set_alpha(alpha)
        self.surface.blit(logo, logo_rect)

    def _draw_menu(
        self,
        items: list[str],
        font: pygame.font.Font,
        line_height: int,
        menu_start_y: int,
        alpha: int = 255,
        alignment: str = "center",
        x: int = 2,
        highlight: bool = True
    ) -> None:
        """Render menu items centered horizontally, highlight the selected one.

        Args:
            font: The font used for the menu.
            line_height: Vertical spacing between items in pixels.
            menu_start_y: Y coordinate of the first menu item center.
        """
        for i, el in enumerate(items):
            if highlight:
                color = Color.RED if i == self.menu_index else Color.WHITE
            else:
                color = Color.WHITE
            sub = font.render(el, True, color)
            sub_rect = sub.get_rect(
                **{alignment: (self.width // x, menu_start_y + i * line_height)}
            )
            sub.set_alpha(alpha)
            self.surface.blit(sub, sub_rect)
