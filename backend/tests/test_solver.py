import pytest
from backend.app.cube.engine import CubeEngine
from backend.app.solver.kociemba_solver import KociembaSolver
from backend.app.cube.constants import SOLVED_STATE


def test_solver_solved_cube():
    solver = KociembaSolver()
    solution = solver.solve(SOLVED_STATE)
    assert solution == []


def test_solver_inverse_hint():
    solver = KociembaSolver()
    engine = CubeEngine()
    moves = ["R", "U", "R'", "U'"]
    engine.apply_moves(moves)
    solution = solver.solve(engine.get_state(), hint_history=moves)
    engine.apply_moves(solution)
    assert engine.is_solved()


def test_solver_bfs_short_scramble():
    solver = KociembaSolver()
    engine = CubeEngine()
    engine.apply_moves(["F", "R"])
    solution = solver.solve(engine.get_state())
    assert solution is not None
    engine.apply_moves(solution)
    assert engine.is_solved()
