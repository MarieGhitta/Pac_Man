"""Cheat configuration screens for title and pause contexts."""


import pygame

from src.game.cheat import Cheat
from src.ui.screens.screen import Screen
from src.utils.color import Color
from src.utils.screen_state import ScreenState


class CheatScreen(Screen):
    """Cheat toggle menu accessible from the title screen."""

    def __init__(self, surface: pygame.surface.Surface, cheat: Cheat):
        """Initialize the cheat screen.

        Args:
            surface: Target pygame surface.
            cheat: Shared cheat flags instance.
        """
        super().__init__(surface)
        self.cheat = cheat
        self.menu_items = [
            "Invincibility",
            "Ghost Freeze",
            "Speed Boost",
            "Infinite Time",
            "Infinite Lives"
        ]
        self.cheat_attrs = [
            "invincibility",
            "ghost_freeze",
            "speed_boost",
            "infinite_time",
            "infinite_lives"
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Toggle cheats on RETURN, navigate on arrows, exit on ESCAPE.

        Args:
            event: Pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    attr = self.cheat_attrs[self.menu_index]
                    setattr(self.cheat, attr, not getattr(self.cheat, attr))
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.TITLE

    def update(self, current_time: int) -> None:
        """No-op: cheat screen has no animated state.

        Args:
            current_time: Current time in milliseconds (unused).
        """

    def draw(self) -> None:
        """Render the cheat toggle menu with ON/OFF status column."""
        self.surface.fill(Color.BLACK)
        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height // 2 - total_height // 3
        self._draw_menu(
            self.menu_items,
            self.font,
            line_height,
            menu_start_y,
            255,
            "midleft",
            4
        )
        for i, attr in enumerate(self.cheat_attrs):
            state = getattr(self.cheat, attr)
            status = "ON" if state else "OFF"
            color = Color.RED if i == self.menu_index else Color.WHITE
            sub = self.font.render(status, True, color)
            sub_rect = sub.get_rect(
                midleft=(self.width * 2 // 3, menu_start_y + i * line_height)
            )
            self.surface.blit(sub, sub_rect)


class PauseCheatScreen(CheatScreen):
    """Extended cheat menu accessible from the pause screen."""

    def __init__(self, surface: pygame.surface.Surface, cheat: Cheat):
        """Initialize the pause cheat screen with action items.

        Args:
            surface: Target pygame surface.
            cheat: Shared cheat flags instance.
        """
        super().__init__(surface, cheat)
        self.overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.overlay.fill(Color.ALPHA_BLACK)
        self.menu_items = [
            "Invincibility",
            "Ghost Freeze",
            "Speed Boost",
            "Infinite Time",
            "Infinite Lives",
            "Add Life",
            "Level Skip",
            "Instant Win",
            "Instant Lose"

        ]
        self.cheat_attrs = [
            "invincibility",
            "ghost_freeze",
            "speed_boost",
            "infinite_time",
            "infinite_lives",
            "add_lives"
        ]
        self.lives_menu: list[int] = [1, 3, 5, 10]
        self.lives_index: int = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle toggles, Add Life cycling, actions, and ESCAPE.

        Args:
            event: Pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    if self.menu_index < 5:
                        attr = self.cheat_attrs[self.menu_index]
                        setattr(
                            self.cheat, attr, not getattr(self.cheat, attr)
                        )
                    else:
                        match self.menu_index:
                            case 5:
                                self.cheat.add_lives = (
                                    self.lives_menu[self.lives_index]
                                )
                                self.next_screen = ScreenState.RESUME
                            case 6:
                                self.cheat.lvl_skip = True
                                self.next_screen = ScreenState.GAME
                            case 7:
                                self.cheat.instant_win = True
                                self.next_screen = ScreenState.END
                            case 8:
                                self.cheat.instant_lose = True
                                self.next_screen = ScreenState.END
                case pygame.K_LEFT:
                    if self.menu_index == 5:
                        self.lives_index = (
                            (self.lives_index - 1) % len(self.lives_menu)
                        )
                case pygame.K_RIGHT:
                    if self.menu_index == 5:
                        self.lives_index = (
                            (self.lives_index + 1) % len(self.lives_menu)
                        )
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.PAUSE

    def update(self, current_time: int) -> None:
        """No-op: pause cheat screen has no animated state.

        Args:
            current_time: Current time in milliseconds (unused).
        """

    def draw(self) -> None:
        """Render the overlay and extended cheat menu."""
        self.surface.blit(self.overlay, (0, 0))
        line_height = int(self.font.get_height() * 1.5)
        total_height = len(self.menu_items) * line_height
        menu_start_y = self.height // 2 - total_height // 3
        self._draw_menu(
            self.menu_items,
            self.font,
            line_height,
            menu_start_y,
            255,
            "midleft",
            4
        )
        for i, attr in enumerate(self.cheat_attrs):
            state = getattr(self.cheat, attr)
            if attr == "add_lives":
                status = str(self.lives_menu[self.lives_index])
            else:
                status = "ON" if state else "OFF"
            color = Color.RED if i == self.menu_index else Color.WHITE
            sub = self.font.render(status, True, color)
            sub_rect = sub.get_rect(
                midleft=(self.width * 2 // 3, menu_start_y + i * line_height)
            )
            self.surface.blit(sub, sub_rect)
