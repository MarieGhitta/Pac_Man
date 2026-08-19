"""Entry point for the Pac-Man game."""

import pygame

from src.config.loader import ConfigLoader
from src.game.direction import Direction
from src.game.game import Game
from src.renderer.renderer import Renderer
from src.ui.highscore import Highscore


def main() -> None:
    """Run the game."""
    try:
        pygame.init()
        config = ConfigLoader().load("config.json")
        highscore = Highscore(config.highscore_filename)
        highscore.add_score({"username": "Zara", "score": 1200})
        highscore.add_score({"username": "Luc", "score": 8500})
        highscore.add_score({"username": "Nina", "score": 300})
        highscore.add_score({"username": "Tom", "score": 15000})
        highscore.add_score({"username": "Eva", "score": 4200})
        highscore.add_score({"username": "Max", "score": 750})
        highscore.add_score({"username": "Ines", "score": 22000})
        highscore.add_score({"username": "Paul", "score": 6300})
        highscore.add_score({"username": "Sara", "score": 100})
        highscore.add_score({"username": "Nico", "score": 9800})
        highscore.add_score({"username": "Lea", "score": 3300})
        highscore.add_score({"username": "Hugo", "score": 18500})
        highscore.add_score({"username": "Mia", "score": 550})
        highscore.add_score({"username": "Alex", "score": 12000})
        highscore.add_score({"username": "Jade", "score": 7100})
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
                        game.player.next_direction = Direction.UP
                    elif event.key == pygame.K_RIGHT:
                        game.player.next_direction = Direction.RIGHT
                    elif event.key == pygame.K_DOWN:
                        game.player.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT:
                        game.player.next_direction = Direction.LEFT
            game.update()
            renderer.draw(game)
            clock.tick(60)
        pygame.quit()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except pygame.error as e:
        print(f"Pygame error: {e}")


if __name__ == "__main__":
    main()
