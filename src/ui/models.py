"""Player score model with input validation."""


class PlayerScore():
    """Validated player score entry."""

    def __init__(self, username: str, score: int) -> None:
        """Initialize and validate a player score.

        Args:
            username: Alphanumeric name, 3 to 10 characters.
            score: Non-negative integer score.

        Raises:
            ValueError: If username or score fails validation.
        """
        self.username: str = self._validate_username(username)
        self.score: int = self._validate_score(score)

    def _validate_username(self, username: str) -> str:
        """Validate and return the username.

        Args:
            username: Name to validate.

        Returns:
            The validated username.

        Raises:
            ValueError: If username is not alnum or is out of length bounds.
        """
        if not username.isalnum():
            raise ValueError("username must be alphanumeric")
        username_length = len(username)
        if username_length < 3 or username_length > 10:
            raise ValueError("username must be between 3 and 10 characters")
        return username

    def _validate_score(self, score: int) -> int:
        """Validate and return the score.

        Args:
            score: Score to validate.

        Returns:
            The validated score.

        Raises:
            ValueError: If score is negative.
        """
        if score < 0:
            raise ValueError("score must be non-negative")
        return score
