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
            highscore_filename (str): The file with scores.
            levels (list[LevelConfig]): THe list of levels.
            lives (int): The number of lives.
            pacgum (int): The number of pacgums.
            points_per_pacgum (int): Points of pacgum.
            points_per_super_pacgum (int): Points per super pacgum.
            points_per_ghost (int): points per ghost.
            seed (int): The seed.
            level_max_time (int): Max time per level.
        """
        self.highscore_filename = highscore_filename
        self.levels = levels
        self.lives: int = lives
        self.pacgum = pacgum
        self.points_per_pacgum = points_per_pacgum
        self.points_per_ghost = points_per_ghost
        self.seed = seed
        self.level_max_time = level_max_time
        self.points_per_super_pacgum = points_per_super_pacgum
