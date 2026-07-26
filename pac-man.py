"""Entry point for the Pac-Man game."""

import pygame
from src.config.loader import ConfigLoader
from src.game.game import Game
from src.renderer.renderer import Renderer
from src.game.direction import Direction


def main() -> None:
    try:
        config = ConfigLoader().load("config.json")
        game = Game(config)
        renderer = Renderer(game.level)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.move_player(Direction.UP)
                    elif event.key == pygame.K_RIGHT:
                        game.move_player(Direction.RIGHT)
                    elif event.key == pygame.K_DOWN:
                        game.move_player(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        game.move_player(Direction.LEFT)

            renderer.draw(game)
            clock.tick(60)
        pygame.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
