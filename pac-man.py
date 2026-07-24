"""Entry point for the Pac-Man game."""

import pygame
from src.config.loader import ConfigLoader
from src.game.game import Game
from src.renderer.renderer import Renderer


def main() -> None:
    config = ConfigLoader().load("config.json")
    game = Game(config)
    renderer = Renderer(game.level)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        renderer.draw(game)
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
