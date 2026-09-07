"""Manage persistent highscores stored in a JSON file."""


import json

from pathlib import Path

from src.ui.models import PlayerScore


class Highscore():
    """Top 10 highscore system backed by a JSON file."""

    def __init__(self, path: str) -> None:
        """Initialize the highscore system and load existing scores.

        Args:
            path: Path to the JSON highscore file.

        Raises:
            ValueError: If the file exists but contains invalid JSON.
        """
        self.path = path
        self.scores: list[dict[str, str | int]] = []
        self._check_file()

    def _check_file(self) -> None:
        """Load scores from file, or create an empty file if absent.

        Raises:
            ValueError: If the file is corrupted or cannot be read/created.
        """
        if Path(self.path).exists():
            try:
                with open(self.path, 'r') as f:
                    self.scores = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"corrupted highscore file: {e}") from e
            except OSError as e:
                raise ValueError(f"cannot read highscore file: {e}") from e
        else:
            try:
                with open(self.path, 'w') as f:
                    json.dump([], f)
            except OSError as e:
                raise ValueError(f"cannot create highscore file: {e}") from e

    def add_score(self, player: PlayerScore) -> int | None:
        """Add a score, keep the top 10, and persist to disk.

        Args:
            player: valid player object with username and score.

        Returns:
            Index of the entry in the sorted top 10, or None.

        Raises:
            ValueError: If the highscore file cannot be written.
        """
        entry: dict[str, str | int] = {
            "username": player.username, "score": player.score
        }
        self.scores.append(entry)
        self.scores = sorted(
            self.scores,
            key=lambda n: n["score"],
            reverse=True
        )[:10]
        try:
            with open(self.path, "w") as f:
                json.dump(self.scores, f, indent=4)
        except OSError as e:
            raise ValueError(f"cannot save highscore file: {e}") from e
        for i, item in enumerate(self.scores):
            if item is entry:
                return i
        return None
