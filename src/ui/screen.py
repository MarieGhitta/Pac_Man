"""Abstract base class for game screens."""


from abc import ABC, abstractmethod

import pygame


class Screen(ABC):
    """Abstract base class for all game screens.

    Each concrete screen manages its own input handling, state update,
    and rendering. Set `next_screen` to signal a transition to the manager.
    """

    def __init__(self) -> None:
        """Initialize the screen with no pending transition."""
        self.next_screen: str | None = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        pass

    @abstractmethod
    def update(self, current_time: int) -> None:
        """Advance the screen's internal state.

        Args:
            current_time: Current time in milliseconds.
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Render the screen onto the given surface.

        Args:
            surface: The pygame surface to draw onto.
        """
        pass


class TitleScreen(Screen):
    """Title screen with logo, animation, and main menu."""

    def __init__(self, surface: pygame.surface.Surface) -> None:
        """Initialize the title screen.

        Args:
            surface: The pygame surface to draw onto.
        """
        super().__init__()
        self.surface = surface
        self.width: int = surface.get_width()
        self.height: int = surface.get_height()
        self.title_font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/CrackMan.ttf", self.height // 8
        )
        self.font: pygame.font.Font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", self.height // 16
        )
        self.menu_items: list[str] = [
            "Play", "Highscores", "Cheat Mode", "Quit"
        ]
        self.menu_index: int = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        """Process a single pygame event.

        Args:
            event: The pygame event to handle (key press, QUIT, etc.).
        """
        pass

    def update(self, current_time: int) -> None:
        """Advance the screen's internal state.

        Args:
            current_time: Current time in milliseconds.
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """Render the screen onto the given surface.

        Args:
            surface: The pygame surface to draw onto.
        """
        self.surface.fill((0, 0, 0))
        logo = self.title_font.render("Pac-Man", True, (255, 191, 0))
        logo_rect = logo.get_rect(center=(self.width // 2, self.height // 4))
        surface.blit(logo, logo_rect)
