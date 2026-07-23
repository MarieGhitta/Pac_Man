"""Entry point for the Pac-Man game."""
from src.maze.generator import MazeFactory
from src.config.loader import ConfigLoader
from src.game.game import Game


def main():
    config = ConfigLoader().load("config.json")
    print(config.lives)
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
