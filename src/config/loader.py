"""Load the game configuration."""

import json
from typing import Any
from src.config.models import Config, LevelConfig


class ConfigLoader:
    """Load the game configuration."""

    def _remove_comments(self, content: str) -> str:
        clean_lines = []
        for line in content.splitlines():
            if (line.strip().startswith("#")
               or line.strip().startswith("//")):
                continue
            clean_lines.append(line)
        return "\n".join(clean_lines)
    
    def _get_int(self, data: dict[str, Any],
                 key: str,
                 default: int,
                 minimum: int | None = None) -> int:
        value = data.get(key, default)
        if not isinstance(value, int):
            print(f"Invalid '{key}', using default ({default}).")
            return default
        if minimum is not None and value < minimum:
            print(f"Invalid '{key}', using default ({default}).")
            return default
        return value
    
    def _get_str(self, data: dict[str, Any],
                 key: str,
                 default: str) -> str:
        value = data.get(key, default)
        if not isinstance(value, str):
            print(f"Invalid '{key}', using default ({default}).")
            return default
        return value
    
    def _build_level(self,
                     data: dict[str, Any]) -> LevelConfig:
        width=self._get_int(data, "width", 20, minimum=1)
        height=self._get_int(data, "height", 20, minimum=1)
        return LevelConfig(width, height)
    

    def _build_config(self, data: dict[str, Any]) -> Config:
        highscore_filename = self._get_str(data, "highscore_filename",
                                      "highscores.json")
        lives = self._get_int(data, "lives", 3, minimum=1)
        pacgum = self._get_int(data, "pacgum", 42, minimum=0)
        points_per_pacgum = self._get_int(data, "points_per_pacgum", 10, minimum=0)
        points_per_super_pacgum = self._get_int(data, "points_per_super_pacgum", 50, minimum=0)
        points_per_ghost = self._get_int(data, "points_per_ghost", 200, minimum=0)
        seed = self._get_int(data, "seed", 42)
        level_max_time = self._get_int(data, "level_max_time", 90, minimum=1)
        levels_data = data.get("levels", [])
        if not isinstance(levels_data, list):
            print("Invalid 'levels', using default ([]).")
            levels_data = []
        levels = []
        for level in levels_data:
            if isinstance(level, dict):
                levels.append(self._build_level(level))
            else:
                print("Invalid level configuration, skipping level.")
        return Config(
            highscore_filename=highscore_filename,
            levels=levels,
            lives=lives,
            pacgum=pacgum,
            points_per_pacgum=points_per_pacgum,
            points_per_super_pacgum=points_per_super_pacgum,
            points_per_ghost=points_per_ghost,
            seed=seed,
            level_max_time=level_max_time
        )

    def load(self, path: str) -> Config:
        """Load the configuration from a file."""
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            content = self._remove_comments(content)
            data = json.loads(content)
            if not isinstance(data, dict):
                raise ValueError("Configuration must be a JSON object.")
            return self._build_config(data)
        except FileNotFoundError as e:
            raise ValueError("Configuration file not found.") from e
        except json.JSONDecodeError as e:
            raise ValueError("Invalid configuration file.") from e
