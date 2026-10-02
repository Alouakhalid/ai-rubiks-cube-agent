import pytest
from backend.app.cube.engine import CubeEngine
from backend.app.cube.constants import SOLVED_STATE, VALID_MOVES


def test_initial_cube_is_solved():
    engine = CubeEngine()
    assert engine.is_solved()
    assert engine.get_state() == SOLVED_STATE


def test_move_reversibility():
    engine = CubeEngine()
    engine.apply_move("R")
    assert not engine.is_solved()
    engine.apply_move("R'")
    assert engine.is_solved()
    assert engine.get_state() == SOLVED_STATE


def test_four_rotations_cycle():
    for move in ["U", "D", "L", "R", "F", "B"]:
        engine = CubeEngine()
        for _ in range(4):
            engine.apply_move(move)
        assert engine.is_solved()
        assert engine.get_state() == SOLVED_STATE


def test_double_turns():
    for move in ["U", "D", "L", "R", "F", "B"]:
        engine = CubeEngine()
        engine.apply_move(f"{move}2")
        engine.apply_move(f"{move}2")
        assert engine.is_solved()


def test_scramble_generates_unsolved_state():
    engine = CubeEngine()
    moves = engine.scramble(length=20)
    assert len(moves) == 20
    assert not engine.is_solved()
    assert len(engine.get_state()) == 54


def test_reset_restores_solved_state():
    engine = CubeEngine()
    engine.scramble(length=15)
    assert not engine.is_solved()
    engine.reset()
    assert engine.is_solved()
    assert engine.get_state() == SOLVED_STATE
