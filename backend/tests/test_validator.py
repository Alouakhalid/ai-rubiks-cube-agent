import pytest
from backend.app.cube.validator import CubeValidator
from backend.app.cube.constants import SOLVED_STATE


def test_solved_state_is_valid():
    res = CubeValidator.validate_state(SOLVED_STATE)
    assert res.is_valid
    assert "physically valid" in res.message


def test_invalid_length():
    res = CubeValidator.validate_state("UUUU")
    assert not res.is_valid
    assert "54 stickers" in res.message


def test_invalid_sticker_counts():
    invalid_counts = "U" * 10 + "R" * 8 + "F" * 9 + "D" * 9 + "L" * 9 + "B" * 9
    res = CubeValidator.validate_state(invalid_counts)
    assert not res.is_valid
    assert "Face 'U' has 10 stickers" in res.message


def test_duplicate_centers():
    invalid_centers = list(SOLVED_STATE)
    invalid_centers[4] = "R"
    invalid_centers[13] = "R"
    res = CubeValidator.validate_state("".join(invalid_centers))
    assert not res.is_valid
