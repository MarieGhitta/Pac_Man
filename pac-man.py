"""Entry point for the Pac-Man game."""


import sys

import pygame

from src.app import App


def main() -> None:
    """Run the game."""
    try:
        argc = len(sys.argv)
        if argc != 2:
            print("Missing argument for the program to run")
            sys.exit()
        config = sys.argv[1]
        app = App(config)
        app.run()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except pygame.error as e:
        print(f"Pygame error: {e}")


if __name__ == "__main__":
    main()
