"""Entry point for the Pac-Man game."""


import pygame

from src.app import App


def main() -> None:
    """Run the game."""
    try:
        app = App("config.json")
        app.run()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except pygame.error as e:
        print(f"Pygame error: {e}")


if __name__ == "__main__":
    main()
