"""Entry point for the Pac-Man game."""


import pygame

from src.config.loader import ConfigLoader
from src.game.direction import Direction
from src.game.game import Game
from src.renderer.renderer import Renderer
from src.ui.highscore import Highscore
from src.ui.models import PlayerScore
from src.ui.screen import TitleScreen


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
        renderer = Renderer(game.level, surface)
        clock = pygame.time.Clock()
        running = True
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
                                    running = False

            match screen_state:
                case "title":
                    title_screen.update(current_time)
                    title_screen.draw(surface)
                    match title_screen.next_screen:
                        case "game":
                            screen_state = "game"
                        case "highscores":
                            pass
                        case "cheat":
                            pass
                        case "quit":
                            running = False
                case "game":
                    game.update()
                    renderer.draw(game)

            pygame.display.flip()
            clock.tick(60)

        player = PlayerScore("AAA", game.score)
        highscore.add_score(player)
        pygame.quit()

    except ValueError as e:
        print(f"Configuration error: {e}")
    except pygame.error as e:
        print(f"Pygame error: {e}")


if __name__ == "__main__":
    main()
