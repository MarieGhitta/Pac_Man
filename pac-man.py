"""Entry point for the Pac-Man game."""
from src.config.loader import ConfigLoader

def main() -> None:
    loader = ConfigLoader()

    try:
        config = loader.load("config.json")
    except ValueError as error:
        print(error)
        return

    print("Configuration loaded successfully!")
    print(f"Highscore file: {config.highscore_filename}")
    print(f"Lives: {config.lives}")
    print(f"Pacgum: {config.pacgum}")
    print(f"Number of levels: {len(config.levels)}")

    for index, level in enumerate(config.levels, start=1):
        print(f"Level {index}: {level.width}x{level.height}")


if __name__ == "__main__":
    main()