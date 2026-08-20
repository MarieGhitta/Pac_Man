"""Entry point for the Pac-Man game."""


import pygame

from src.config.loader import ConfigLoader
from src.game.direction import Direction
from src.game.game import Game
from src.renderer.renderer import Renderer
from src.ui.highscore import Highscore
from src.ui.models import PlayerScore


def main() -> None:
    """Run the game."""
    try:
        pygame.init()
        config = ConfigLoader().load("config.json")
        highscore = Highscore(config.highscore_filename)
        game = Game(config)
        renderer = Renderer(game.level)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
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
            game.update()
            renderer.draw(game)
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
