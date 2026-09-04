"""Configure a Level."""


class LevelConfig:
    """Represent the configuration of a level."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize a level configuration.

        Args:
            width: Width of the level.
            height: Height of the level.
        """
        self.width: int = width
        self.height: int = height


class Config:
    """Represents the game configuration."""

    def __init__(
        self,
        highscore_filename: str,
        levels: list[LevelConfig],
        max_levels: int,
        lives: int,
        pacgum: int,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int,
        seed: int,
        level_max_time: int,
    ) -> None:
        """Initialize the game configuration.

        Args:
            highscore_filename: Path to the highscore JSON file.
            levels: List of level configurations.
            max_levels: Total number of levels in a game.
            lives: Starting number of lives.
            pacgum: Number of pacgums to place (0 = fill all).
            points_per_pacgum: Points awarded per pacgum collected.
            points_per_super_pacgum: Points awarded per super-pacgum collected.
            points_per_ghost: Base points awarded per ghost eaten.
            seed: RNG seed for level 1 maze generation.
            level_max_time: Time limit per level in seconds.
        """
        self.highscore_filename = highscore_filename
        self.levels = levels
        self.max_levels = max_levels
        self.lives: int = lives
        self.pacgum = pacgum
        self.points_per_pacgum = points_per_pacgum
        self.points_per_ghost = points_per_ghost
        self.seed = seed
        self.level_max_time = level_max_time
        self.points_per_super_pacgum = points_per_super_pacgum
