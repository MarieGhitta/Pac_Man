from enum import Enum, auto
import pygame

from src.config.loader import ConfigLoader
from src.config.models import Config
from src.game.direction import Direction
from src.game.engine import Engine
from src.renderer.renderer import Renderer
from src.ui.highscore import Highscore
from src.ui.screens.screen import Screen
from src.ui.screens.title_screen import TitleScreen
from src.ui.screens.pause_screen import PauseScreen
from src.ui.screens.end_screen import EndScreen
from src.ui.screens.highscore_screen import HighscoreScreen


class ScreenState(Enum):
    TITLE = auto()
    CHEAT = auto()
    GAME = auto()
    PAUSE = auto()
    HIGHSCORE = auto()
    END = auto()


class App:

    def __init__(self, config_path: str = "config.json") -> None:
        pygame.init()
        info = pygame.display.Info()
        self.surface: pygame.surface.Surface = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN | pygame.SCALED
        )
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.config: Config = ConfigLoader().load(config_path)
        self.engine: Engine = Engine(self.config)
        self.renderer: Renderer = Renderer(self.engine.level, self.surface)
        self.highscore: Highscore = Highscore(self.config.highscore_filename)
        self.screens: dict[ScreenState, Screen | None] = {
            ScreenState.TITLE: TitleScreen(self.surface),
            ScreenState.CHEAT: None,
            ScreenState.GAME: None,
            ScreenState.PAUSE: PauseScreen(self.surface),
            ScreenState.HIGHSCORE: HighscoreScreen(
                self.surface, self.highscore.scores
            ),
            ScreenState.END: None
        }
        self.screen_state: ScreenState = ScreenState.TITLE
        self.frozen_frame: pygame.surface.Surface | None = None
        self.running: bool = True
        self.score_saved: bool = False
        self.endgame_score_display: bool = False


    def run(self) -> None:
        while self.running:
            current_time = pygame.time.get_ticks()
            self._handle_events(current_time)
            self._update(current_time)
            self._handle_transitions(current_time)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self, current_time: int) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            match self.screen_state:

                case ScreenState.TITLE:
                    if screen := self.screens[ScreenState.TITLE]:
                        screen.handle_event(event)

                case ScreenState.CHEAT:
                    pass

                case ScreenState.GAME:
                    if event.type == pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_UP:
                                self.engine.player.next_direction = Direction.UP
                            case pygame.K_RIGHT:
                                self.engine.player.next_direction = Direction.RIGHT
                            case pygame.K_DOWN:
                                self.engine.player.next_direction = Direction.DOWN
                            case pygame.K_LEFT:
                                self.engine.player.next_direction = Direction.LEFT
                            case pygame.K_ESCAPE:
                                self.frozen_frame = self.surface.copy()
                                self.screen_state = ScreenState.PAUSE
                                self.engine.on_pause(current_time)
                            case pygame.K_q:
                                self.running = False

                case ScreenState.PAUSE:
                    if screen := self.screens[ScreenState.PAUSE]:
                        screen.handle_event(event)

                case ScreenState.HIGHSCORE:
                    if screen := self.screens[ScreenState.HIGHSCORE]:
                        screen.handle_event(event)

                case ScreenState.END:
                    if screen := self.screens[ScreenState.END]:
                        screen.handle_event(event)


    def _update(self, current_time: int) -> None:
        pass


    def _handle_transitions(self, current_time: int) -> None:
        pass
