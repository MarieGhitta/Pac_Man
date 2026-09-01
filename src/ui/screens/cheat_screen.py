import pygame

from src.game.cheat import Cheat
from src.ui.screens.screen import Screen
from src.utils.color import Color
from src.utils.screen_state import ScreenState


class CheatScreen(Screen):
   
    def __init__(self, surface: pygame.surface.Surface, cheat: Cheat):
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
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    match self.menu_index:
                        case 0:
                            self.cheat.invincibility = not self.cheat.invincibility
                        case 1:
                            self.cheat.ghost_freeze = not self.cheat.ghost_freeze 
                        case 2:
                            self.cheat.speed_boost = not self.cheat.speed_boost
                        case 3:
                            self.cheat.infinite_time = not self.cheat.infinite_time
                        case 4:
                            self.cheat.infinite_lives = not self.cheat.infinite_lives
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.TITLE


    def update(self, current_time: int) -> None:
        pass

    def draw(self) -> None:
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
   
    def __init__(self, surface: pygame.surface.Surface, cheat: Cheat):
        super().__init__(surface, cheat)
        self.menu_items = [
            "Invincibility",
            "Ghost Freeze",
            "Speed Boost",
            "Infinite Time",
            "Level Skip",

        ]
        self.cheat_attrs = [
            "invincibility",
            "ghost_freeze",
            "speed_boost",
            "infinite_time",
        ]
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._navigate(event.key)
            match event.key:
                case pygame.K_RETURN:
                    match self.menu_index:
                        case 0:
                            self.cheat.invincibility = not self.cheat.invincibility
                        case 1:
                            self.cheat.ghost_freeze = not self.cheat.ghost_freeze 
                        case 2:
                            self.cheat.speed_boost = not self.cheat.speed_boost
                        case 3:
                            self.cheat.infinite_time = not self.cheat.infinite_time
                case pygame.K_ESCAPE:
                    self.next_screen = ScreenState.PAUSE


    def update(self, current_time: int) -> None:
        pass

    def draw(self) -> None:
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
