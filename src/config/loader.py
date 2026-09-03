"""Load the game configuration."""


import json
from typing import Any

from src.config.models import Config, LevelConfig


class ConfigLoader:
    """Load the game configuration."""

    def _remove_comments(self, content: str) -> str:
        """Strip lines starting with '#' or '//' from a JSON string.

        Args:
            content: Raw file content.

        Returns:
            Content with comment lines removed.
        """
        clean_lines = []
        for line in content.splitlines():
            if (line.strip().startswith("#")
               or line.strip().startswith("//")):
                continue
            clean_lines.append(line)
        return "\n".join(clean_lines)

    def _get_int(
        self,
        data: dict[str, Any],
        key: str,
        default: int,
        minimum: int | None = None,
        maximum: int | None = None
    ) -> int:
        """Extract an integer from a config dict, falling back to default.

        Args:
            data: Config dictionary.
            key: Key to look up.
            default: Value returned if key is missing or invalid.
            minimum: Inclusive lower bound.
            maximum: Inclusive upper bound.

        Returns:
            Validated integer value.
        """
        value = data.get(key, default)
        if not isinstance(value, int):
            print(f"Invalid '{key}', using default ({default}).")
            return default
        if minimum is not None and value < minimum:
            print(f"Invalid '{key}', using default ({default}).")
            return default
        if maximum is not None and value > maximum:
            print(f"Invalid '{key}', using default ({default}).")
            return default
        return value

    def _get_str(
        self, data: dict[str, Any], key: str, default: str
    ) -> str:
        """Extract a string from a config dict, falling back to default.

        Args:
            data: Config dictionary.
            key: Key to look up.
            default: Value returned if key is missing or invalid.

        Returns:
            Validated string value.
        """
        value = data.get(key, default)
        if not isinstance(value, str):
            print(f"Invalid '{key}', using default ({default}).")
            return default
        return value

    def _build_level(self, data: dict[str, Any]) -> LevelConfig:
        """Build a LevelConfig from a raw level dict.

        Args:
            data: Level configuration dictionary.

        Returns:
            Validated LevelConfig instance.
        """
        width = self._get_int(data, "width", 15, 3, 101)
        height = self._get_int(data, "height", 19, 3, 101)
        return LevelConfig(width, height)

    def _build_config(self, data: dict[str, Any]) -> Config:
        """Build a Config from a raw config dict.

        Args:
            data: Top-level configuration dictionary.

        Returns:
            Validated Config instance.

        Raises:
            ValueError: If no valid levels are found.
        """
        highscore_filename = self._get_str(
            data, "highscore_filename", "highscores.json"
        )
        max_levels = self._get_int(data, "max_levels", 10, 10, 99)
        lives = self._get_int(data, "lives", 3, 1, 99)
        pacgum = self._get_int(data, "pacgum", 0, 0)
        points_per_pacgum = self._get_int(
            data, "points_per_pacgum", 10, 0, 100
        )
        points_per_super_pacgum = self._get_int(
            data, "points_per_super_pacgum", 50, 0, 500
        )
        points_per_ghost = self._get_int(
            data, "points_per_ghost", 200, 0, 2000
        )
        seed = self._get_int(data, "seed", 42)
        level_max_time = self._get_int(data, "level_max_time", 90, 10, 90)
        levels_data = data.get("levels", [])
        if not isinstance(levels_data, list):
            print("Invalid 'levels', using default ([]).")
            levels_data = []
        levels = []
        for level in levels_data:
            if isinstance(level, dict):
                levels.append(self._build_level(level))
            else:
                print("invalid level configuration, skipping level.")
        if not levels:
            raise ValueError("configuration must have at least one level")
        return Config(
            highscore_filename=highscore_filename,
            levels=levels,
            max_levels=max_levels,
            lives=lives,
            pacgum=pacgum,
            points_per_pacgum=points_per_pacgum,
            points_per_super_pacgum=points_per_super_pacgum,
            points_per_ghost=points_per_ghost,
            seed=seed,
            level_max_time=level_max_time
        )

    def load(self, path: str) -> Config:
        """Load and validate the configuration from a JSON file.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            Validated Config instance.

        Raises:
            ValueError: If file missing, invalid JSON, or no levels.
        """
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            content = self._remove_comments(content)
            data = json.loads(content)
            if not isinstance(data, dict):
                raise ValueError("configuration must be a JSON object")
            return self._build_config(data)
        except FileNotFoundError as e:
            raise ValueError("configuration file not found") from e
        except json.JSONDecodeError as e:
            raise ValueError("invalid configuration file") from e
