"""Load the game configuration."""

import json
from typing import Any
from config.models import Config


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

    def _build_config(self, data: dict[str, Any]) -> Config:
        highscore_filename = data.get("highscore_filename",
                                      "highscores.json")
        lives = data.get("lives", 3)
        pacgum = data.get("pacgum", 42)
        points_per_pacgum = data.get("points_per_pacgum", 10)
        points_per_super_pacgum = data.get("points_per_super_pacgum", 50)
        points_per_ghost = data.get("points_per_ghost", 200)
        seed = data.get("seed", 42)
        level_max_time = data.get("level_max_time", 90)
        levels = []
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

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            content = self._remove_comments(content)
            data = json.loads(content)
        return self._build_config(data)
