"""Configure a Level."""

class LevelConfig:
    """Represent the configuration of a level."""
    def __init__(self, width: int, height: int) -> None:
        """Initialize a level configuration.

        Args:
            width: width of the level.
            height: height of the level.
        """
        self.width = width
        self.height = height

class Config:
    """Represents the game configuration."""
    def __init__(
            self,
            highscore_filename: str,
            levels: list[LevelConfig],
            lives: int,
            pacgum: int,
            points_per_pacgum: int,
            points_per_super_pacgum: int,
            points_per_ghost: int,
            seed: int,
            level_max_time: int,
    ) -> None:
        self.highscore_filename = highscore_filename
        self.levels = levels
        self.lives = lives
        self.pacgum = pacgum
        self.points_per_pacgum = points_per_pacgum
        self.points_per_ghost = points_per_ghost
        self.seed = seed
        self.level_max_time = level_max_time
        self.points_per_super_pacgum = points_per_super_pacgum