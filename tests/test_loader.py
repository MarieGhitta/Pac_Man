import pytest

from src.config.loader import ConfigLoader


def test_load_valid_config() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/valid_config.json")

    assert config.highscore_filename == "highscores.json"
    assert config.lives == 3
    assert config.pacgum == 42
    assert len(config.levels) == 1
    assert config.levels[0].width == 20
    assert config.levels[0].height == 20

def test_invalid_json_raises_value_error() -> None:
    loader = ConfigLoader()

    with pytest.raises(ValueError, match="Invalid configuration file."):
        loader.load("tests/resources/invalid_json.json")
    
def test_missing_file_raises_value_error() -> None:
    loader = ConfigLoader()

    with pytest.raises(ValueError, match="Configuration file not found."):
        loader.load("tests/resources/does_not_exist.json")

def test_invalid_lives_uses_default() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/invalid_lives.json")

    assert config.lives == 3

def test_invalid_levels_uses_empty_list() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/invalid_levels.json")

    assert config.levels == []

def test_invalid_level_is_skipped() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/invalid_level.json")

    assert len(config.levels) == 2
    assert config.levels[0].width == 20
    assert config.levels[1].width == 15

def test_invalid_width_uses_default() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/invalid_width.json")

    assert config.levels[0].width == 20

def test_invalid_root_raises_value_error() -> None:
    loader = ConfigLoader()

    with pytest.raises(
        ValueError,
        match="Configuration must be a JSON object.",
    ):
        loader.load("tests/resources/invalid_root.json")

def test_comment_skipped() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/comment.json")

    assert config.lives == 5

def test_invalid_key() -> None:
    loader = ConfigLoader()

    config = loader.load("tests/resources/invalid_key.json")
    assert config.lives == 3
