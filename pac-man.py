"""Entry point for the Pac-Man game."""


import pygame

from src.config.loader import ConfigLoader
from src.game.direction import Direction
from src.game.game import Game
from src.renderer.renderer import Renderer
from src.ui.end_screen import EndScreen
from src.ui.highscore import Highscore
from src.ui.models import PlayerScore
from src.ui.pause_menu import PauseMenu
from src.ui.title_screen import TitleScreen


def main() -> None:
    """Run the game."""
    try:
        pygame.init()
        info = pygame.display.Info()
        surface = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN | pygame.SCALED
        )
        config = ConfigLoader().load("config.json")
        highscore = Highscore(config.highscore_filename)
        game = Game(config)
        screen_state = "title"
        title_screen = TitleScreen(surface)
        end_screen: EndScreen | None = None
        pause_menu = PauseMenu(surface)
        renderer = Renderer(game.level, surface)
        clock = pygame.time.Clock()
        running = True
        frozen_frame: pygame.surface.Surface | None = None
        score_saved: bool = False
        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                match screen_state:
                    case "title":
                        title_screen.handle_event(event)
                    case "game":
                        if event.type == pygame.KEYDOWN:
                            match event.key:
                                case pygame.K_UP:
                                    game.player.next_direction = Direction.UP
                                case pygame.K_RIGHT:
                                    game.player.next_direction = Direction.RIGHT
                                case pygame.K_DOWN:
                                    game.player.next_direction = Direction.DOWN
                                case pygame.K_LEFT:
                                    game.player.next_direction = Direction.LEFT
                                case pygame.K_ESCAPE:
                                    frozen_frame = surface.copy()
                                    screen_state = "pause"
                                    game.on_pause(current_time)
                                case pygame.K_q:
                                    running = False
                    case "pause":
                        pause_menu.handle_event(event)
                    case "lose":
                        if end_screen is not None:
                            end_screen.handle_event(event)

            match screen_state:
                case "title":
                    title_screen.update(current_time)
                    title_screen.draw()
                    if title_screen.next_screen is not None:
                        match title_screen.next_screen:
                            case "game":
                                title_screen.menu_index = 0
                                game = Game(config)
                                renderer = Renderer(game.level, surface)
                                screen_state = "game"
                                score_saved = False
                            case "highscores":
                                pass
                            case "cheat":
                                pass
                            case "quit":
                                running = False
                        title_screen.next_screen = None
                case "game":
                    game.update()
                    if game.game_over:
                        end_screen = EndScreen(surface, current_time)
                        screen_state = "lose"
                    renderer.draw(game)
                case "pause":
                    pause_menu.update(current_time)
                    if frozen_frame is not None:
                        surface.blit(frozen_frame, (0, 0))
                    pause_menu.draw()
                    if pause_menu.next_screen is not None:
                        match pause_menu.next_screen:
                            case "game":
                                game.on_resume(current_time)
                                screen_state = "game"
                            case "title":
                                pause_menu.menu_index = 0
                                screen_state = "title"
                            case "quit":
                                running = False
                        pause_menu.next_screen = None
                case "lose":
                    if end_screen is not None:
                        if end_screen.can_navigate and not score_saved:
                            player = PlayerScore(
                                end_screen.username, game.score
                            )
                            highscore.add_score(player)
                            score_saved = True
                        end_screen.update(current_time)
                        end_screen.draw()
                        if end_screen.next_screen is not None:
                            match end_screen.next_screen:
                                case "game":
                                    title_screen.menu_index = 0
                                    game = Game(config)
                                    renderer = Renderer(game.level, surface)
                                    screen_state = "game"
                                    score_saved = False
                                case "title":
                                    pause_menu.menu_index = 0
                                    screen_state = "title"
                                case "quit":
                                    running = False
                            end_screen.next_screen = None

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    except ValueError as e:
        print(f"Configuration error: {e}")
    except pygame.error as e:
        print(f"Pygame error: {e}")


if __name__ == "__main__":
    main()
