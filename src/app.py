import pygame

from src.config.loader import ConfigLoader
from src.config.models import Config
from src.game.engine import Engine
from src.renderer.renderer import Renderer
from src.ui.highscore import Highscore
from src.ui.models import PlayerScore
from src.ui.screens.screen import Screen
from src.ui.screens.title_screen import TitleScreen
from src.ui.screens.pause_screen import PauseScreen
from src.ui.screens.end_screen import EndScreen
from src.ui.screens.highscore_screen import HighscoreScreen
from src.ui.screens.game_screen import GameScreen
from src.utils.screen_state import ScreenState


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
            ScreenState.GAME: GameScreen(
                self.surface, self.engine, self.renderer
            ),
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
            self._handle_events()
            self._update(current_time)
            self._handle_transitions(current_time)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if screen := self.screens[self.screen_state]:
                screen.handle_event(event)


    def _update(self, current_time: int) -> None:
        match self.screen_state:
            case ScreenState.TITLE:
                if screen := self.screens[self.screen_state]:
                    screen.update(current_time)
                    screen.draw()
            case ScreenState.GAME:
                if screen := self.screens[self.screen_state]:
                    screen.update(current_time)
                    screen.draw()
            case ScreenState.PAUSE:
                if self.frozen_frame is not None:
                    self.surface.blit(self.frozen_frame, (0, 0))
                if screen := self.screens[self.screen_state]:
                    screen.update(current_time)
                    screen.draw()
            case ScreenState.END:
                if screen := self.screens[self.screen_state]:
                    screen.update(current_time)
                    screen.draw()
            case ScreenState.HIGHSCORE:
                if screen := self.screens[ScreenState.HIGHSCORE]:
                    screen.update(current_time)
                    screen.draw()

    def _handle_transitions(self, current_time: int) -> None:
        screen = self.screens[self.screen_state]
        if screen is None or screen.next_screen is None:
            return
        match screen.next_screen:
            case ScreenState.TITLE:
                if title := self.screens[ScreenState.TITLE]:
                    title.menu_index = 0
                self.screen_state = ScreenState.TITLE
            case ScreenState.CHEAT:
                pass
            case ScreenState.GAME:
                self.engine = Engine(self.config)
                self.renderer = Renderer(self.engine.level, self.surface)
                self.screens[ScreenState.GAME] = GameScreen(
                    self.surface, self.engine, self.renderer
                )
                self.screen_state = ScreenState.GAME
                self.score_saved = False
            case ScreenState.PAUSE:
                if pause := self.screens[ScreenState.PAUSE]:
                    pause.menu_index = 0
                self.frozen_frame = self.surface.copy()
                self.engine.on_pause(current_time)
                self.screen_state = ScreenState.PAUSE
            case ScreenState.RESUME:
                self.engine.on_resume(current_time)
                self.screen_state = ScreenState.GAME
            case ScreenState.HIGHSCORE:
                if self.screen_state == ScreenState.END:
                    self.endgame_score_display = True
                if self.endgame_score_display and not self.score_saved:
                    end_screen = self.screens[ScreenState.END]
                    if end_screen and isinstance(end_screen, EndScreen):
                        player = PlayerScore(end_screen.username, self.engine.score)
                        last_score = self.highscore.add_score(player)
                        if hs := self.screens[ScreenState.HIGHSCORE]:
                            if isinstance(hs, HighscoreScreen):
                                hs.scores = self.highscore.scores
                                hs.last_score = last_score
                        self.score_saved = True
                self.screen_state = ScreenState.HIGHSCORE
            case ScreenState.END:
                ending = "win"
                if self.engine.game_over:
                    ending = "lose"
                self.screens[ScreenState.END] = EndScreen(
                    self.surface, current_time, ending
                )
                self.screen_state = ScreenState.END
            case ScreenState.QUIT:
                self.running = False
        screen.next_screen = None
