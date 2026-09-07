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
            ValueError: If the file is corrupted, malformed, or cannot be
                read/created.
        """
        if Path(self.path).exists():
            try:
                with open(self.path, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"corrupted highscore file: {e}") from e
            except OSError as e:
                raise ValueError(f"cannot read highscore file: {e}") from e
            if not self._is_valid_scores(data):
                raise ValueError(
                    "malformed highscore file: expected a list of "
                    "{username: str, score: int} entries"
                )
            self.scores = data
        else:
            try:
                with open(self.path, 'w') as f:
                    json.dump([], f)
            except OSError as e:
                raise ValueError(f"cannot create highscore file: {e}") from e

    def _is_valid_scores(self, data: object) -> bool:
        """Return whether data has the expected top-10 score list shape.

        Args:
            data: Parsed JSON value to validate.

        Returns:
            True if data is a list of well-formed score entries.
        """
        if not isinstance(data, list):
            return False
        for entry in data:
            if not isinstance(entry, dict):
                return False
            if not isinstance(entry.get("username"), str):
                return False
            if not isinstance(entry.get("score"), int):
                return False
        return True

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
