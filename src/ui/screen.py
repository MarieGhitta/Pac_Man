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
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__()
        self.width: int = surface.get_width()
        self.height: int = surface.get_height()
        self.title_font: pygame.font.Font = pygame.font.Font(None, 96)
        self.font: pygame.font.Font = pygame.font.Font(None, 48)
        self.menu_items: list[str] = [
            "Play", "Highscores", "Cheat Mode", "Quit"
        ]
        self.menu_index: int = 0


    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, current_time: int) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass
