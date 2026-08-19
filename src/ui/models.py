class PlayerScore():
    def __init__(self, username: str, score: int) -> None:
        self.username: str = self._validate_username(username)
        self.score: int = self._validate_score(score)

    def _validate_username(self, username: str) -> str:
        if not username.isalnum():
            raise ValueError("username must be alphanumeric")
        username_length = len(username)
        if username_length < 3 or username_length > 10:
            raise ValueError("username must be between 3 and 10 characters")
        return username

    def _validate_score(self, score: int) -> int:
        if score < 0:
            raise ValueError("score must be non-negative")
        return score
