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
        """Load scores from file, or create an empty file if absent."""
        if Path(self.path).exists():
            try:
                with open(self.path, 'r') as f:
                    self.scores = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"corrupted highscore file: {e}")
        else:
            with open(self.path, 'w') as f:
                json.dump([], f)

    def add_score(self, player: PlayerScore) -> int | None:
        """Add a score, keep the top 10, and persist to disk.

        Args:
            username: player name.
            score: player score.
        """
        self.scores.append(
            {"username": player.username, "score": player.score}
        )
        sorted_scores = sorted(
            self.scores,
            key=lambda n: n["score"],
            reverse=True
        )
        self.scores = sorted_scores[:10]
        with open(self.path, "w") as f:
            json.dump(
                self.scores,
                f,
                indent=4
            )
        entry = {"username": player.username, "score": player.score}
        return self.scores.index(entry) if entry in self.scores else None
