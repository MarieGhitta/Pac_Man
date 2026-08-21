"""Abstract base class for game screens."""


from abc import ABC, abstractmethod

import pygame

from src.utils.color import Color


class Screen(ABC):
    """Abstract base class for all game screens.

    Each concrete screen manages its own input handling, state update,
    and rendering. Set `next_screen` to signal a transition to the manager.
    """

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the screen with no pending transition."""
        self.next_screen: str | None = None
        self.surface = surface
        self.width: int = surface.get_width()
        self.height: int = surface.get_height()
        self.font_size: int = self.height // 32
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.font_size
        )
        self.menu_items: list[str] = []
        self.menu_index: int = 0

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        pass

    def _navigate(self, key: int) -> None:
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

    def _draw_menu(self, line_height: int, menu_start_y: int) -> None:
        for i, el in enumerate(self.menu_items):
            color = Color.RED if i == self.menu_index else Color.WHITE
            sub = self.font.render(el, True, color)
            sub_rect = sub.get_rect(
                center=(self.width // 2, menu_start_y + i * line_height)
            )
            self.surface.blit(sub, sub_rect)
